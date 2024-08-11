Иногда бывает нужно быстро развернуть приложение, не беспокоясь о масштабируемости. В этом случае можно развернуть приложение на одном сервере. Этот подход работает для небольших и средних приложений, staging- или dev-окружений, где высокая доступность не является необходимостью. В этой статье я покажу, как настроить [Kamal](https://kamal-deploy.org/) для развертывания приложения на одном сервере с сертификатом TLS от Let's Encrypt. Преимущество этого подхода в том, что когда придет время, вы можете добавить балансировщик нагрузки перед приложением и масштабировать его на несколько серверов.

Мы рассмотрим конфигурацию развертывания, подготовим сервер и выполним первое развертывание. Мы также кратко рассмотрим, как можно управлять приложением на сервере. Наконец, мы настроим полный процесс CI для автоматического развертывания нашего приложения на сервере из GitHub Actions.

### Обзор сервиса

В качестве примера сервиса будем использовать простой http-сервис на python, который будет отвечать HTTP-статусом 200 на любой запрос на порт `80`.

```dockerfile
FROM python:3
WORKDIR /app
EXPOSE 80
CMD ["python", "-m", "http.server", "80"]
```

Наш сервис не использует базу данных для фокусирования внимания на деплоее, но для примера мы запустим базу данных PostgerSQL и добавим в конфигурацию сервиса переменую окружения с данным о соединении с базой, как если бы наше приложение ее действительно использовало.

### Конфигурация развертывания

Kamal - это относительно тонкая обертка вокруг Docker, поэтому почти все можно настроить под свои нужды. В нем есть предустановленные скрипты для начальной настройки серверов с установкой cURL и Docker. Также имеется конфигурация по умолчанию для Traefik, который используется в качестве реверс-прокси для маршрутизации всего трафика к приложению. Кроме того, есть удобный инструмент командной строки для управления сервисом на хосте: сборка, развертывание, чтение логов, выполнение команд и т.д.

Давайте рассмотрим полную конфигурацию развертывания для Kamal, которая включает Traefik, веб-приложение и конфигурацию базы данных.

_config/deploy.yaml_
```yaml
service: kamal-example
image: <%= ENV['REGISTRY_USERNAME'] %>/kamal-example

servers:
  web:
    hosts:
      - <%= ENV['SERVER_IP'] %>
    labels:
      traefik.http.routers.kamal-example.rule: Host(`<%= ENV['APP_DOMAIN'] %>`)
      traefik.http.routers.kamal-example.tls: true
      traefik.http.routers.kamal-example.entrypoints: websecure
      traefik.http.routers.kamal-example.tls.certresolver: letsencrypt
    options:
      network: "traefik"

registry:
  server: ghcr.io
  username:
    - REGISTRY_USERNAME
  password:
    - REGISTRY_PASSWORD

builder:
  multiarch: false
  cache:
    type: gha
    options: mode=max

healthcheck:
  path: /health
  port: 80
  max_attempts: 15
  interval: 30s

env:
  secret:
    - DATABASE_URL

# Database
accessories:
 db:
   image: postgres:15.2-alpine3.17
   host: <%= ENV['SERVER_IP'] %>
   env:
     secret:
       - POSTGRES_DB
       - POSTGRES_USER
       - POSTGRES_PASSWORD
   directories:
     - kamal_example_postgres_data:/var/lib/postgresql/data
   options:
     network: "traefik"

# Traefik
traefik:
  options:
    publish:
      - "443:443"
    network: "traefik"
    volume:
      - "/root/letsencrypt:/letsencrypt"
  args:
    entrypoints.web.address: ":80"
    entrypoints.websecure.address: ":443"
    # Конфигурация TLS
    certificatesResolvers.letsencrypt.acme.email: <%= ENV['TRAEFIK_ACME_EMAIL'] %>
    certificatesResolvers.letsencrypt.acme.storage: "/letsencrypt/acme.json"
    certificatesResolvers.letsencrypt.acme.tlschallenge: true
    certificatesResolvers.letsencrypt.acme.httpchallenge.entrypoint: web
    # Редирект на HTTPS по умолчанию
    entryPoints.web.http.redirections.entryPoint.to: websecure
    entryPoints.web.http.redirections.entryPoint.scheme: https
    entryPoints.web.http.redirections.entrypoint.permanent: true
```

Мы настроили Traefik с дополнительными аргументами, начинающимися с `certificatesResolvers`, и директорией для автоматического добавления TLS-сертификатов с использованием Let's Encrypt. Кроме того, мы включили пару аргументов `entryPoints` для автоматической перенаправления с `http` на `https`.

Мы добавили конфигурацию веб-сервиса с метками Traefik для настройки домена для приложения:
```yaml
servers:
  web:
    hosts:
      - <%= ENV['SERVER_IP'] %>
    labels:
      traefik.http.routers.kamal-example.rule: Host

(`<%= ENV['APP_DOMAIN'] %>`)
      traefik.http.routers.kamal-example.tls: true
      traefik.http.routers.kamal-example.entrypoints: websecure
      traefik.http.routers.kamal-example.tls.certresolver: letsencrypt
    options:
      network: "traefik"
```
Мы будем считывать IP-адрес сервера из переменной окружения, поэтому используем синтаксис шаблона Ruby для этого: `<%= ENV['SERVER_IP'] %>`. Если вы хотите развернуть приложение на нескольких серверах, вы можете считывать несколько IP-адресов из одной переменной окружения, содержащей строку с IP-адресами, разделенными запятыми, и затем считывать их в конфигурации так: `hosts: <%= ENV['SERVER_IPS'].split(',') %>`.

Наше приложение содержит только начальную настройку с подключением к базе данных, поэтому в данный момент нам нужно настроить только переменную окружения `DATABASE_URL`:
```yaml
env:
  secret:
    - DATABASE_URL
```

Мы запускаем базу данных в качестве дополнительного сервиса (`accessories`) на том же хосте, с конфигурациями для секретов и директорий для хранения данных, поэтому для всех сервисов используем одну и ту же сеть Docker, которую в нашем случае назовем `traefik`. Это имя сети может быть любым. Пользовательская сеть Docker необходима для того, чтобы приложение могло получить доступ к базе данных, работающей на **том же хосте**. Таким образом, если вы запускаете базу данных на другом хосте или используете сторонний сервис, такой как Supabase или Neon, вам не нужно настраивать сеть Docker.

Мы будем использовать GitHub registry для хранения Docker-образов нашего приложения. Можно использовать любой registry-сервис, который вам удобен - просто измените значение `registry.server`.

Мы будем использовать Kamal для сборки Docker-образа приложения и GitHub Actions в качестве нашего сервиса CI, который включает конфигурацию для кэширования, чтобы ускорить сборки. Мы будем развертывать на архитектуре amd64, поэтому чтобы избежать потери времени на сборку нескольких образов для каждой платформы, самое простое решение - отключить сборку для нескольких архитектур:

```yaml
builder:
  multiarch: false
  cache:
    type: gha
    options: mode=max
```

Наконец, мы настроили конфигурацию проверки работоспособности с пользовательскими параметрами пути, порта и попыток:

```yaml
healthcheck:
  path: /health
  port: 80
  max_attempts: 15
  interval: 30s
```

### Первоначальное развертывание

Прежде всего, нам нужно подготовить сервер с начальной установкой и развертыванием приложения и других сервисов.

#### Необходимые условия

- Установленный Docker на локальной машине.
- Сервер с публичным IP.
- Домен, направленный на сервер.
- SSH-подключение с локальной машины к серверу с использованием SSH-ключей.
- Открытые порты 443 и 80 на сервере.
- (Опционально) Настройка файрвола для открытия только портов 443, 80 и 22.

#### Установка Kamal локально

Для упрощения установки зависимостей мы будем использовать `mise-en-place`. Установите [mise-en-place](https://mise.jdx.dev/getting-started.html#quickstart) (или [asdf](https://asdf-vm.com/guide/getting-started.html)).

В корене проекта нужно создать файл с версиями утилит, которые хотим установить. В нашем случае это Ruby:

_.tool-versions_
```
ruby 3.3.0
```

Затем выполните команду:

```shell
brew install libyaml  # или на Ubuntu: `sudo apt-get install libyaml-dev` 
mise install ruby
gem install kamal -v 1.8.0
kamal version
```

#### Переменные окружения

Создайте файл `.env` со всеми необходимыми переменными окружения с актуальными значениями для развертывания на сервере:

```shell
# Generated by kamal envify
# DEPLOY
SERVER_IP=192.168.0.1
REGISTRY_USERNAME=your-username
REGISTRY_PASSWORD=secret-registry-password
TRAEFIK_ACME_EMAIL=your_email@example.com
APP_DOMAIN=app.domain.com

# App
DATABASE_URL="postgres://postgres:secret-db-password@kamal-example-db:5432/demo"

# DB accessory
POSTGRES_DB=demo
POSTGRES_USER=demoadmin
POSTGRES_PASSWORD=secret-db-password
```

Примечания:
- `SERVER_IP` - IP-адрес сервера, на который вы хотите развернуть приложение. Вы должны иметь возможность подключиться к нему с помощью SSH-ключей.
- `REGISTRY_USERNAME` и `REGISTRY_PASSWORD` - учетные данные для Docker-реестра. В нашем случае мы используем `ghcr.io`, но это может быть любой реестр.
- `TRAEFIK_ACME_EMAIL` - email для регистрации TLS-сертификата с Let's Encrypt и Traefik.
- `APP_DOMAIN` - домен вашего приложения, который должен быть настроен для указания на `SERVER_IP`.
- `kamal-example-db` - имя контейнера базы данных из раздела аксессуаров файла `deploy/config.yml`.
- Мы дублируем учетные данные базы данных для настройки контейнера базы данных и использования `DATABASE_URL` в приложении.

**Примечание:** _Не включайте файл `.env` в репозиторий git!_

#### Настройка сервера и развертывание приложения

Установите Docker на сервер:

```shell
kamal server bootstrap
```

Создайте сеть Docker для доступа к контейнеру базы данных из приложения по имени контейнера
и каталог для сертификатов Let's Encrypt:

```shell
ssh user@192.168.0.1 'docker network create traefik'
ssh user@192.168.0.1 'mkdir -p /root/letsencrypt && touch /root/letsencrypt/acme.json && chmod 600 /root/letsencrypt/acme.json'
```

Настройте Traefik, базу данных, переменные окружения, соберите/отправьте образ приложения и запустите приложение на сервере:

```shell
kamal setup
```

Теперь приложение полностью развернуто на сервере! Вы можете проверить его на своем домене.

#### Регулярное развертывание

Для последующих развертываний с локальной машины выполните команду:

```shell
kamal deploy
```

Автоматическое развертывание с помощью GitHub Actions рассмотрим его подробнее в следующем разделе.

### Управление приложением на сервере

Давайте рассмотрим несколько полезных команд для управления и проверки нашего приложения на сервере.

Получение списка запущенных контейнеров:

```shell
kamal details -q

Traefik Host: 192.168.0.1
CONTAINER ID   IMAGE           COMMAND                  CREATED       STATUS       PORTS                                                                      NAMES
045e76b559e3   traefik:v2.10   "/entrypoint.sh --pr…"   3 weeks ago   Up 3 weeks   0.0.0.0:80->80/tcp, :::80->80/tcp, 0.0.0.0:443->443/tcp, :::443->443/tcp   traefik

App Host: 192.168.0.1
CONTAINER ID   IMAGE                                                                                   COMMAND                  CREATED          STATUS                    PORTS     NAMES
e1007ae82d0b   ghcr.io/demouser/kamal-example:f0dce409b7cde87a22597a56f3f23e8a24374215   "/__cacert_entrypoin…"   12 minutes ago   Up 12 minutes (healthy)   80/tcp    kamal-example-web-f0dce409b7cde87a22597a56f3f23e8a24374215

Accessory db Host: 192.168.0.1
CONTAINER ID   IMAGE                      COMMAND                  CREATED       STATUS       PORTS                                       NAMES
da9d0b805330   postgres:15.2-alpine3.17   "docker-entrypoint.s…"   3 weeks ago   Up 3 weeks   5432/tcp   kamal-example-db
```

Просмотр логов приложения:

```shell
kamal app logs -f
...
```

Запуск интерактивной оболочки в текущем запущенном контейнере:

```shell
kamal app exec -i --reuse sh
Get current version of running container...
  ...
Launching interactive command with version f0dce409b7cde87a22597a56f3f23e8a24374215 via SSH from existing container on 192.168.0.1...
/app # 
```

Вывод версии приложения:

```shell
kamal app version

...
  INFO [9dcdfdb6] Finished in 1.311 seconds with exit status 0 (successful).
App Host: 192.168.0.1
f0dce409b7cde87a22597a56f3f23e8a24374215
```

Остановка или запуск текущей версии приложения:

```shell
kamal app stop
kamal app start
```

Если вы хотите изменить конфигурацию traefik, выполните команду:

```shell
kamal traefik reboot
```

И несколько других команд, которые вы можете найти, выполнив:

```shell
kamal help
```

### CI

На данный момент у нас есть приложение, работающее на сервере, и возможность развертывать и управлять им с локальной машины. Следующий шаг - развернуть приложение из CI-пайплайна.

#### CI пайплайн: переменные окружения

Для настройки CI необходимо добавить следующие переменные окружения в качестве секретов для Actions. В интерфейсе GitHub репозитория перейдите к `Settings -> Secrets and variables -> Actions`. Затем добавьте переменные с теми же значениями, которые вы добавили в локальный файл `.env`:

```shell
APP_DOMAIN
DATABASE_URL
POSTGRES_DB
POSTGRES_PASSWORD
POSTGRES_USER
SERVER_IP
SSH_PRIVATE_KEY
TRAEFIK_ACME_EMAIL
```

- `SSH_PRIVATE_KEY` - новый SSH-приватный ключ **без пароля**, который вы создали и добавили его публичную часть в `~/.ssh/authorized_keys` сервера для авторизации с CI-воркера.

Для генерации SSH-ключей выполните команду:

```shell
ssh-keygen -t ed25519 -C "your_email@example.com"
```

#### CI пайплайн: развертывание
Как я уже упоминал ранее, мы используем GitHub Actions, поэтому давайте рассмотрим конфигурацию развертывания:

_.github/workflows/deploy.yaml_
```yaml
name: Deploy

on:
  push:
    branches: [ master ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    timeout-minutes: 20
    steps:
      - uses: actions/checkout@v4
      - uses: jdx/mise-action@v2
      - uses: webfactory/ssh-agent@v0.9.0
        with:
          ssh-private-key: ${{ secrets.SSH_PRIVATE_KEY }}

      - name: Setup Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Expose GitHub Runtime for cache
        uses: crazy-max/ghaction-github-runtime@v3

      - name: Install kamal
        run: gem install kamal -v 1.5.2

      - name: Push env vars
        env:
          SERVER_IP: ${{ secrets.SERVER_IP }}
          REGISTRY_USERNAME: ${{ github.repository_owner }}
          REGISTRY_PASSWORD: ${{ github.token }}
          TRAEFIK_ACME_EMAIL: ${{ secrets.TRAEFIK_ACME_EMAIL }}
          APP_DOMAIN: ${{ secrets.APP_DOMAIN }}
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
          POSTGRES_DB: ${{ secrets.POSTGRES_DB }}
          POSTGRES_USER: ${{ secrets.POSTGRES_USER }}
          POSTGRES_PASSWORD: ${{ secrets.POSTGRES_PASSWORD }}
        run: kamal envify

      - name: Deploy
        run: kamal deploy --version=${{ github.sha }}

      - name: Kamal Release
        if: ${{ cancelled() }}
        run: kamal lock release
```

Нам нужно предоставить разрешения на отправку Docker-образов в реестр ghcr.io:
```yaml
jobs:
  deploy:
    ...
    permissions:
      contents: read
      packages: write
```

Для общей защиты от зависания шагов давайте ограничим наш пайплайн 20 минутами:

```yaml
jobs:
  deploy:
    ...
    timeout-minutes: 20
```

Мы используем шаг `- uses: jdx/mise-action@v2` для установки Ruby и других инструментов. Он кэшируется при первом запуске, 
поэтому обычно этот шаг должен быть быстрым.

Для выполнения команд Kamal на сервере нам нужно установить SSH-соединение:

```yaml
jobs:
  deploy:
    steps:
      ...
      - uses: webfactory/ssh-agent@v0.9.0
        with:
          ssh-private-key: ${{ secrets.SSH_PRIVATE_KEY }}
```

Затем у нас есть несколько шагов для включения кэша Docker и установки Kamal.

Далее нам нужно отправить переменные окружения на сервер с помощью `kamal envify`. Поэтому перед отправкой в мастер-ветку вам нужно настроить секреты в настройках репозитория на GitHub, как описано в разделе "CI пайплайн: переменные окружения" выше.


Выполняем развертывание приложения на сервере:

```shell
kamal deploy --version=${{ github.sha }}
```

Последний шаг - защита от неудачных развертываний; освобождение блокировки для разрешения последующих развертываний:

```shell
kamal lock release
```

### Итоги

Kamal предоставляет достачно простой но при этом гибкий поход для развертывания приложения на сервере. Он прозрачен и позволяет изменять почти любую конфигурацию сервисов. Однако было бы лучше иметь один бинарник вместо установки через Ruby. Также я бы избегал SSH-соединения с CI-воркера на сервер, но это, вероятно, разумный компромисс, учитывая простоту деплоя.

Возможные улучшения общей установки приложения, которые выходят за рамки этой статьи:
- Периодическое резервное копирование базы данных (например, с использованием [`postgres-backup-s3`](https://github.com/eeshugerman/postgres-backup-s3?ref=luizkowalski.net) или аналогичного).
- Непривилегированный пользователь в [контейнере](https://kamal-deploy.org/docs/configuration/ssh/#using-a-different-ssh-user-than-root).
- Сбор метрик и логов.
- Использование базы данных как сервиса вместо запуска собственной.

В этой статье я постарался сохранить баланс между отсутствием слишком большого количества деталей и описанием идеи процесса развертывания, сосредоточив внимание на последнем. В любом случае, вы всегда можете ознакомиться документацией [Kamal](https://kamal-deploy.org/docs/installation/) для получения большей ясности. В целом, я рад поделиться полным решением для настройки и запуска приложения на сервере. Надеюсь, это будет полезно или хотя бы послужит вдохновением для вашей собственной настройки деплоя!
