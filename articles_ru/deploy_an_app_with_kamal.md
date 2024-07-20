### Краткое содержание

Для быстрого примера настройки приложения на Clojure с полной конфигурацией развертывания, включающей API-сервис, фронтенд с ClojureScript и PostgreSQL, ознакомьтесь с репозиторием проекта [clojure-kamal-example](https://github.com/abogoyavlensky/clojure-kamal-example). Чтобы попробовать развернуть приложение самостоятельно, просто клонируйте репозиторий и следуйте разделу [Deploy: summary](https://github.com/abogoyavlensky/clojure-kamal-example/tree/master?tab=readme-ov-file#deploy-summary). Если у вас уже есть Docker-образ, который открывает порт 80, вы можете пропустить обзор настройки проекта и перейти прямо к разделу "Deployment config".

### Обзор

Иногда мне нужно быстро развернуть приложение, не беспокоясь о масштабируемости. В этом случае можно развернуть приложение на одном сервере. Этот подход подходит для небольших/средних некритичных приложений, стадийных или предварительных сред. В этой статье я покажу, как настроить [Kamal](https://kamal-deploy.org/) для развертывания полнофункционального Clojure/Script-приложения на одном сервере с сертификатом TLS от Let's Encrypt. Преимущество этого подхода в том, что когда придет время, вы можете добавить балансировщик нагрузки перед приложением и масштабировать его на несколько серверов.

Я начну с выделения важных частей настройки приложения. Затем мы рассмотрим конфигурацию развертывания, подготовим сервер и выполним первое развертывание. Мы также кратко рассмотрим, как можно управлять приложением на сервере. Наконец, мы настроим полный процесс CI для автоматического развертывания нашего приложения на сервере из GitHub Actions.

### Обзор настройки проекта

Мы будем настраивать веб-приложение с Clojure API-сервером на бэкенде, ClojureScript с Re-frame на фронтенде и PostgreSQL в качестве основной базы данных. Вы можете ознакомиться с примером проекта в репозитории [clojure-kamal-example](https://github.com/abogoyavlensky/clojure-kamal-example). Важные части структуры проекта выглядят так:

```text
clojure-kamal-example
├── README.md
├── .tool-versions
├── Dockerfile
├── Taskfile.yaml
├── deps.edn
├── build.clj
├── package.json
├── shadow-cljs.edn
├── tailwind.config.js
├── .github
│   ├── actions/
│   └── workflows
│       ├── checks.yaml
│       └── deploy.yaml
├── config
│   └── deploy.yml
├── dev
│   └── user.clj
├── resources
│   └── db
│   │   ├── migrations/
│   │   └── models.edn
│   ├── public
│   │   ├── css
│   │   │   └── input.css
│   │   └── index.html
│   ├── config.edn
│   └── logback.xml
├── src
│   ├── clj
│   │   └── api
│   │       ├── util/
│   │       ├── db.clj 
│   │       ├── handler.clj 
│   │       ├── server.clj 
│   │       └── main.clj 
│   ├── cljc
│   │   └── common
│   │       └── api_routes.cljc
│   └── cljs
│       └── ui
│           ├── util/
│           ├── db.cljs
│           ├── events.cljs
│           ├── router.cljs
│           ├── subs.cljs
│           ├── views.cljs
│           └── main.cljs
└── test/
```

Здесь мы используем общие названия `api`, `ui` и `common` для префиксов пространства имен каждой части приложения. Мне нравится этот подход, так как он унифицирует части и облегчает переключение между различными проектами.

Говоря о [библиотеках](https://github.com/abogoyavlensky/clojure-kamal-example/blob/master/deps.edn) и [инструментах](https://github.com/abogoyavlensky/clojure-kamal-example/blob/master/.tool-versions), мы используем: [Integrant](https://github.com/weavejester/integrant) для управления системой приложения, [Reitit](https://github.com/metosin/reitit) для маршрутизации на бэкенде и фронтенде, [Malli](https://github.com/metosin/malli) для проверки данных и [Automigrate](https://github.com/abogoyavlensky/automigrate) для управления миграциями базы данных. На фронтенде мы используем ClojureScript с [Re-frame](https://github.com/day8/re-frame), [Shadow CLJS](https://github.com/thheller/shadow-cljs) в качестве системы сборки и [Tailwind CSS](https://tailwindcss.com/) для стилизации. Для управления приложением локально и в CI мы используем [Taskfile](https://taskfile.dev/) как замену Make и [mise-en-place](https://mise.jdx.dev/) для управления версиями системных инструментов.

Для демонстрации я добавил несколько [моделей](https://github.com/abogoyavlensky/clojure-kamal-example/blob/master/resources/db/models.edn) базы данных: `movie` и `director`, маршрут API для получения всех записей из модели `movie` и отображение этого списка на веб-странице. Маршруты API определены в [общем каталоге cljc](https://github.com/abogoyavlensky/clojure-kamal-example/blob/master/src/cljc/common/api_routes.cljc) для использования маршрутов API на фронтенде по именам из одного источника истины.

#### Бэкенд

Система приложения выглядит так:

_resources/config.edn_
```clojure
{:api.db/db {:options 
             {:jdbc-url #profile {:default #env DATABASE_URL
                                  :test "jdbc:tc:postgresql:15.2-alpine3.17:///testdb?TC_DAEMON=true"}}}

 :api.handler/handler {:options 
                       {:reloaded? #profile {:default false
                                             :dev true}
                        :cache-assets? #profile {:default false
                                                 :prod true}}
                       :db #ig/ref :api.db/db}

 :api.server/server {:options 
                     {:port #profile {:default 8000
                                      :prod 80
                                      :test #free-port true}}
                     :handler #ig/ref :api.handler/handler}}
```

Система содержит три компонента:
- `:api.db/db` - пул подключений к базе данных;
- `:api.handler/handler` - обработчик приложения с API Reitit-маршрутизатором на основе Ring и промежуточных программ;
- `:api.server/server` - сервер Jetty.

Мне нравится подход группировки опций конфигурации компонентов в ключе `:options`, чтобы избежать смешивания их с ссылками на другие компоненты. Мы используем Malli для [проверки](https://github.com/abogoyavlensky/clojure-kamal-example/blob/3799199d5947a0161e23fa3228fb972ec09ee631/src/clj/api/handler.clj#L51-L60) всех параметров конфигурации для каждого компонента системы.

Здесь мы используем [Aero](https://github.com/juxt/aero) для расширения конфигурации системы полезными считывателями данных. Есть считыватель `#profile` для переключения между `dev`, `test` и `prod`; `#env` для чтения переменных окружения. Он расширен считывателем `#ig/ref` из Integrant для использования компонентов в качестве ссылок в других компонентах. Также я добавил [`#free-port`](https://github.com/abogoyavlensky/clojure-kamal-example/blob/3799199d5947a0161e23fa3228fb972ec09ee631/src/clj/api/util/system.clj#L26-L29), чтобы выбрать свободный порт для веб-сервера API при его запуске в тестах.

В [обработчике](https://github.com/abogoyavlensky/clojure-kamal-example/blob/master/src/clj/api/handler.clj) есть опции для автоматической перезагрузки кода бэкенда при любом изменении без перезапуска всей системы с помощью `:reloaded?`, и `:cache-assets?` для включения кэширования статических ресурсов в продакшне. Вы можете прочитать о подходе к автоматической перезагрузке в [связанной статье](https://bogoyavlensky.com/blog/auto-reloading-ring/).

Во время тестов мы автоматически запускаем базу данных в контейнере Docker с использованием функции Testcontainers [JDBC support](https://java.testcontainers.org/modules/databases/jdbc/#using-post

gresql). Все, что нужно, это добавить префикс `tc:` после `jdbc:` в JDBC URL, и Testcontainers будет управлять контейнером базы данных под капотом. Чтобы ускорить тесты, мы используем параметр `TC_DAEMON=true` в JDBC URL для повторного использования одного и того же контейнера для нескольких тестов. Этот контейнер будет автоматически остановлен при завершении работы JVM.

#### Фронтенд

На фронтенде мы используем [`reitit.frontend.easy/start!`](https://github.com/abogoyavlensky/clojure-kamal-example/blob/7f9e07a3bfc44aaa60323a22d6c13ded2a232dd6/src/cljs/ui/router.cljs#L35) для настройки маршрутизатора.
Для рендеринга главной страницы мы используем [`re-frame.core/create-root`](https://github.com/abogoyavlensky/clojure-kamal-example/blob/3799199d5947a0161e23fa3228fb972ec09ee631/src/cljs/ui/main.cljs#L13), чтобы иметь возможность использовать последние версии React
(>= 18.x).

Для сборки CSS для [разработки](https://github.com/abogoyavlensky/clojure-kamal-example/blob/3799199d5947a0161e23fa3228fb972ec09ee631/Taskfile.yaml#L80-L93) и в [продакшне](https://github.com/abogoyavlensky/clojure-kamal-example/blob/3799199d5947a0161e23fa3228fb972ec09ee631/Dockerfile#L19) мы используем библиотеку Tailwind CSS js напрямую через `npx`.

Мы запускаем Shadow CLJS через clojure cli и [конфигурацию сборки](https://github.com/abogoyavlensky/clojure-kamal-example/blob/master/shadow-cljs.edn) с использованием `:deps` в качестве источника всех зависимостей. Мы также включили хеширование JavaScript-файлов в сборке релиза. Чтобы использовать эти хешированные JavaScript-файлы в `index.html`, мы используем существующую функцию [`shadow.html/copy-file`](https://github.com/abogoyavlensky/clojure-kamal-example/blob/3799199d5947a0161e23fa3228fb972ec09ee631/shadow-cljs.edn#L15-L17). Для CSS нет встроенного решения, поэтому я добавил пользовательскую функцию [`build/hash-css`](https://github.com/abogoyavlensky/clojure-kamal-example/blob/23e422e914c4db2126a2880689e5b9757c8efe4b/build.clj#L73-L74), которая добавляет хеш к выходному файлу Tailwind CSS CLI и обновляет CSS-файл в `index.html`.

### Создание docker-образа

[Dockerfile](https://github.com/abogoyavlensky/clojure-kamal-example/blob/master/Dockerfile) основан на Alpine и имеет две простые стадии:

- Стадия сборки: собирает uberjar со всеми минифицированными и хешированными фронтенд-статическими файлами.
- Результирующая стадия: финальный образ с только что созданным uberjar из предыдущей стадии.

```dockerfile
FROM --platform=linux/amd64 clojure:temurin-21-tools-deps-1.11.3.1456-alpine AS build

WORKDIR /app

# Install npm
RUN echo "http://dl-cdn.alpinelinux.org/alpine/v3.20/community" >> /etc/apk/repositories
RUN apk add --update --no-cache npm=10.8.0-r0

# Node deps
COPY package.json package-lock.json /app/
RUN npm i

# Clojure deps
COPY deps.edn  /app/
RUN clojure -P -X:cljs:shadow

# Build ui and uberjar
COPY . /app
RUN npx tailwindcss -i ./resources/public/css/input.css -o ./resources/public/css/output-prod.css --minify \
    && clojure -M:dev:cljs:shadow release app \
    && clojure -T:build build


FROM --platform=linux/amd64 eclipse-temurin:21.0.2_13-jre-alpine
LABEL org.opencontainers.image.source=https://github.com/abogoyavlensky/clojure-kamal-example

WORKDIR /app
COPY --from=build /app/target/standalone.jar /app/standalone.jar
RUN apk add --no-cache curl

EXPOSE 80
CMD ["java", "-Xmx256m", "-jar", "standalone.jar"]
```

Мы будем развертывать на архитектуре amd64, поэтому, чтобы иметь возможность развернуть приложение впервые с macOS с Apple Silicon, мы добавили `--platform=linux/amd64` к определению `FROM`.

На этапе сборки мы поочередно запускаем сборку CSS, JS и uberjar. Мы будем публиковать образы в реестр GitHub ghcr.io, поэтому удобно по умолчанию связывать загруженные образы с репозиторием. Для этого мы добавили `LABEL` к определению финального образа. Мы также добавили опцию `-Xmx256m` к команде Java, что позволяет нам развертывать приложение на небольшом экземпляре. Вы можете расширить и обновить эту конфигурацию по своему усмотрению.

### Конфигурация развертывания

Kamal - это всего лишь тонкая оболочка вокруг Docker, поэтому почти все можно настроить и перенастроить. В нем есть предустановленные скрипты для начальной настройки серверов с установкой cURL и Docker. Также имеется конфигурация по умолчанию для Traefik, который используется в качестве реверс-прокси для маршрутизации всего трафика к приложению. Кроме того, есть удобный инструмент командной строки для управления сервисом на хосте: сборка, развертывание, чтение логов, выполнение команд и т.д.

Давайте рассмотрим полную конфигурацию развертывания для Kamal, которая включает Traefik, веб-приложение и конфигурацию базы данных.

_config/deploy.yaml_
```yaml
service: clojure-kamal-example
image: <%= ENV['REGISTRY_USERNAME'] %>/clojure-kamal-example

servers:
  web:
    hosts:
      - <%= ENV['SERVER_IP'] %>
    labels:
      traefik.http.routers.clojure-kamal-example.rule: Host(`<%= ENV['APP_DOMAIN'] %>`)
      traefik.http.routers.clojure-kamal-example.tls: true
      traefik.http.routers.clojure-kamal-example.entrypoints: websecure
      traefik.http.routers.clojure-kamal-example.tls.certresolver: letsencrypt
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
     - clojure_kamal_example_postgres_data:/var/lib/postgresql/data
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
    # TLS-certificate configuration
    certificatesResolvers.letsencrypt.acme.email: <%= ENV['TRAEFIK_ACME_EMAIL'] %>
    certificatesResolvers.letsencrypt.acme.storage: "/letsencrypt/acme.json"
    certificatesResolvers.letsencrypt.acme.tlschallenge: true
    certificatesResolvers.letsencrypt.acme.httpchallenge.entrypoint: web
    # Redirect to HTTPS by default
    entryPoints.web.http.redirections.entryPoint.to: websecure
    entryPoints.web.http.redirections.entryPoint.scheme: https
    entryPoints.web.http.redirections.entrypoint.permanent: true
```

Мы настроили Traefik с дополнительными аргументами, начинающимися с `certificatesResolvers`, и томом для автоматического добавления TLS-сертификатов с использованием Let's Encrypt. Кроме того, мы включили пару аргументов `entryPoints` для автоматической перенаправления с `http` на `https`.

Мы добавили конфигурацию веб-сервиса с метками Traefik для настройки домена для приложения:
```yaml
servers:
  web:
    hosts:
      - <%= ENV['SERVER_IP'] %>
    labels:
      traefik.http.routers.clojure-kamal-example.rule: Host

(`<%= ENV['APP_DOMAIN'] %>`)
      traefik.http.routers.clojure-kamal-example.tls: true
      traefik.http.routers.clojure-kamal-example.entrypoints: websecure
      traefik.http.routers.clojure-kamal-example.tls.certresolver: letsencrypt
    options:
      network: "traefik"
```
Мы будем считывать IP-адрес сервера из переменной окружения, поэтому используем синтаксис шаблона Ruby для этого: `<%= ENV['SERVER_IP'] %>`. Если вы хотите развернуть приложение на нескольких серверах, вы можете считывать несколько IP-адресов из одной переменной окружения, содержащей строку с IP-адресами, разделенными запятыми, и затем считывать их в конфигурации так: `hosts: <%= ENV['SERVER_IPS'].split(',') %>`.

Наше приложение содержит только начальную настройку с подключением к базе данных, поэтому в данный момент нам нужно настроить только переменную окружения JDBC URL:
```yaml
env:
  secret:
    - DATABASE_URL
```

Мы запускаем базу данных в качестве аксессуара на том же хосте, с конфигурациями для секретов и директорий для хранения данных, поэтому для всех сервисов используем одну и ту же сеть Docker, которую в нашем случае называют `traefik`. Имя сети может быть любым. Пользовательская сеть Docker необходима для того, чтобы приложение могло получить доступ к базе данных, работающей на **том же хосте**. Таким образом, если вы запускаете базу данных на другом хосте или используете сторонний сервис, такой как Supabase или Neon, вам не нужно настраивать сеть Docker.

Мы будем использовать реестр GitHub в качестве Docker-реестра для отправки Docker-образов нашего приложения. Однако возможно использовать любой реестр, который вам удобен; просто измените значение `registry.server`.

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
  exposed_port: 4001
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

Пример конфигурации файрвола для сервера может выглядеть так:
![Firewall config](/assets/images/articles/8_firewall_config.png)

#### Установка Kamal локально

Установите [mise-en-place](https://mise.jdx.dev/getting-started.html#quickstart) (или [asdf](https://asdf-vm.com/guide/getting-started.html)),
и выполните команду:

```shell
brew install libyaml  # или на Ubuntu: `sudo apt-get install libyaml-dev` 
mise install ruby
gem install kamal -v 1.5.2
kamal version
```


---

**Примечание**: _Альтернативно, вы можете использовать докеризированную версию Kamal, запуская предопределенную команду `./kamal.sh` вместо версии Ruby gem. Она в основном работает для начальной настройки сервера, но некоторые команды управления могут работать неправильно. Например, `./kamal.sh app logs -f` или `./kamal.sh build push`._

---


#### Переменные окружения

Выполните команду `envify`, чтобы создать файл `.env` со всеми необходимыми пустыми переменными:

```shell
kamal envify --skip-push
```

Параметр `--skip-push` предотвращает отправку файла `.env` на сервер.

Теперь нам нужно заполнить все переменные окружения в файле `.env` актуальными значениями для развертывания на сервере.
Вот пример:

```shell
# Generated by kamal envify
# DEPLOY
SERVER_IP=192.168.0.1
REGISTRY_USERNAME=your-username
REGISTRY_PASSWORD=secret-registry-password
TRAEFIK_ACME_EMAIL=your_email@example.com
APP_DOMAIN=app.domain.com

# App
DATABASE_URL="jdbc:postgresql://clojure-kamal-example-db:5432/demo?user=demoadmin&password=secret-db-password"

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
- `clojure-kamal-example-db` - имя контейнера базы данных из раздела аксессуаров файла `deploy/config.yml`.
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

Приложение развернуто на сервере, но пока не полностью функционально. Нам нужно применить миграции базы данных:

```shell
kamal app exec 'java -jar standalone.jar migrations'
```

Теперь приложение полностью развернуто на сервере! Вы можете проверить его на своем домене, домашняя страница должна выглядеть примерно так:
![App home page](/assets/images/articles/8_app_home_page.png)

---

#### Примечание о миграциях базы данных в продакшне

В общем, мне не нравится запускать миграции базы данных как часть компонента базы данных в системе приложения, потому что у нас нет полного контроля над процессом миграции. Вместо этого я предпочитаю запускать миграции как отдельный шаг в CI-пайплайне перед развертыванием.

Чтобы иметь возможность запускать миграции в jar-файле, я добавил вторую команду в основную функцию приложения. Automigrate по умолчанию читает переменную окружения `DATABASE_URL` и использует модели и миграции из каталога `resources/db`. Таким образом, по умолчанию нам не нужно ничего настраивать, кроме настройки переменной окружения URL базы данных. Основная функция приложения выглядит так:

_api.main.clj_
```clojure
(ns api.main
  (:gen-class)
  (:require [clojure.tools.logging :as log]
            [integrant.core :as ig]
            [automigrate.core :as automigrate]
            [api.util.system :as system-util]))


(defn- run-system
  [profile]
  (let [profile-name-kw profile
        config (system-util/config profile-name-kw)]
    (log/info "[SYSTEM] System is starting with profile:" profile-name-kw)
    (ig/load-namespaces config)
    (-> config
        (ig/init)
        (system-util/at-shutdown))
    (log/info "[SYSTEM] System has been started successfully.")))


(defn -main
  "Run application system in production env."
  [& args]
  (case (first args)
    "migrations" (automigrate/migrate)
    (run-system :prod)))
```

Запуск jar без аргументов запустит систему приложения на порту 80:
`java -jar standalone.jar`. Если

 нам нужно запустить миграции, просто добавьте аргумент к команде: `java -jar standalone.jar migrations`.

---

#### Регулярное развертывание

Для последующих развертываний с локальной машины выполните команду:

```shell
kamal deploy
```

Или просто выполните push в мастер-ветку, есть пайплайн GitHub Actions, который выполняет
развертывание автоматически `.github/workflows/deploy.yaml`. 
Мы рассмотрим его подробнее в следующем разделе.

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
e1007ae82d0b   ghcr.io/abogoyavlensky/clojure-kamal-example:f0dce409b7cde87a22597a56f3f23e8a24374215   "/__cacert_entrypoin…"   12 minutes ago   Up 12 minutes (healthy)   80/tcp    clojure-kamal-example-web-f0dce409b7cde87a22597a56f3f23e8a24374215

Accessory db Host: 192.168.0.1
CONTAINER ID   IMAGE                      COMMAND                  CREATED       STATUS       PORTS                                       NAMES
da9d0b805330   postgres:15.2-alpine3.17   "docker-entrypoint.s…"   3 weeks ago   Up 3 weeks   5432/tcp   clojure-kamal-example-db
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

Печать версии приложения:

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
  checks:
    uses: ./.github/workflows/checks.yaml

  deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    timeout-minutes: 20
    needs: [ checks ]
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

      - name: Build and push
        run: |
          kamal registry login
          kamal build push --version=${{ github.sha }}

      - name: Migrations
        run:  |
          kamal build pull --version=${{ github.sha }}
          kamal app exec --version=${{ github.sha }} 'java -jar standalone.jar migrations'

      - name: Deploy
        run: kamal deploy --skip-push --version=${{ github.sha }}

      - name: Kamal Release
        if: ${{ cancelled() }}
        run: kamal lock release
```

Перед развертыванием мы запускаем пайплайн с проверкой линтинга, форматирования, устаревших зависимостей и тестов:

```yaml
jobs:
  checks:
    uses: ./.github/workflows/checks.yaml
```
Мы рассмотрим это подробнее в следующем разделе.

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

Проверки должны быть успешно завершены перед развертыванием:

```yaml
jobs:
  deploy:
    ...
    needs: [ checks ]
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

Мы разделили команду `kamal deploy` на два шага, потому что нам нужно запускать миграции базы данных с CI-воркера **до** развертывания новой версии приложения. Для этой цели мы используем аргумент `--version` для каждой команды развертывания.

Сначала собираем Docker-образ и отправляем его в реестр:
```shell
kamal build push --version=${{ github.sha }}
```

Загружаем собранный образ из предыдущего шага и запускаем в нем миграции:

```shell
kamal build pull --version=${{ github.sha }}
kamal app exec --version=${{ github.sha }} 'java -jar standalone.jar migrations'
```

Выполняем фактическое развертывание приложения, но не собираем образ

, используя аргумент `--skip-push`, потому что мы уже собрали и отправили образ:

```shell
kamal deploy --skip-push --version=${{ github.sha }}
```

Это все. Последний шаг - защита от неудачных развертываний; освобождение блокировки для разрешения последующих развертываний:

```shell
kamal lock release
```

#### CI пайплайн: проверки 

Полный пайплайн проверок, который мы запускаем при каждом pull-request и push в мастер, выглядит так:

_.github/workflows/deploy.yaml_
```yaml
name: Checks

on:
  pull_request:
    branches: [ master ]
  workflow_call:

jobs:
  deps:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: jdx/mise-action@v2
      - name: Cache Clojure dev dependencies
        uses: actions/cache@v4
        with:
          path: ~/.m2/repository
          key: ${{ runner.os }}-clojure-dev-${{ hashFiles('**/deps.edn') }}
          restore-keys: ${{ runner.os }}-clojure-dev
      - name: Install Clojure dev deps
        run: task deps

  fmt:
    runs-on: ubuntu-latest
    needs: [ deps ]
    steps:
      - uses: actions/checkout@v4
      - uses: jdx/mise-action@v2
      - name: Fmt
        run: task fmt-check

  lint:
    runs-on: ubuntu-latest
    needs: [ deps ]
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/restore-deps
      - name: Lint
        run: task lint-init && task lint

  outdated:
    runs-on: ubuntu-latest
    needs: [ deps ]
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/restore-deps
      - name: Outdated deps
        run: task outdated-check

  tests:
    runs-on: ubuntu-latest
    needs: [ deps ]
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/restore-deps
      - name: Run tests
        run: task test
```

_.github/actions/restore-deps/action.yaml_
```yaml
name: Install deps
runs:
  using: composite
  steps:
    - uses: jdx/mise-action@v2
    - name: Restore cached clojure dev deps
      uses: actions/cache/restore@v4
      with:
        path: ~/.m2/repository
        key: ${{ runner.os }}-clojure-dev-${{ hashFiles('**/deps.edn') }}
        restore-keys: ${{ runner.os }}-clojure-dev
```

Я не буду останавливаться здесь слишком долго, потому что конфигурация достаточно самоочевидна.
На первом шаге `deps` мы устанавливаем и кэшируем все системные зависимости с помощью `uses: jdx/mise-action@v2`.
Файл `.tool-versions` выглядит так:
```
task 3.34.1
java temurin-21.0.2+13.0.LTS
clojure 1.11.3.1456
node 20.13.1
cljstyle 0.16.626
clj-kondo 2024.05.24
ruby 3.3.0
```
Таким образом, мы используем ту же конфигурацию во время разработки и в CI-пайплайне. 
Затем мы настраиваем кэш для зависимостей Clojure и устанавливаем их:

```yaml
jobs:
  deps:
    steps:
      ...
      - name: Cache Clojure dev dependencies
        uses: actions/cache@v4
        with:
          path: ~/.m2/repository
          key: ${{ runner.os }}-clojure-dev-${{ hashFiles('**/deps.edn') }}
          restore-keys: ${{ runner.os }}-clojure-dev
      - name: Install Clojure dev deps
        run: task deps
```

И повторно используем его на каждом шаге, где нам нужны кэшированные зависимости:

```yaml
jobs:
  deps:
    lint:
      ...
      - uses: ./.github/actions/restore-deps
```

После этого шага мы запускаем шаги `lint`, `fmt`, `outdated` и `tests` параллельно, используя кэш зависимостей Clojure из предыдущего шага. Все команды описаны в `Taskfile.yaml`:

_Taskfile.yaml_
```yaml
tasks:
  ...
  test:
    desc: Run tests
    cmds:
      - clojure -X:dev:cljs:test
      
  fmt:
    desc: Fix code formatting
    cmds:
      - cljstyle fix --report {{ .DIRS }}

  lint-init:
    desc: Linting project's classpath
    cmds:
      - clj-kondo --parallel --dependencies --copy-configs --lint {{ .DIRS }}
    vars:
      DIRS:
        sh: clojure -Spath

  lint:
    desc: Linting project's code
    cmds:
      - clj-kondo --parallel --lint {{ .DIRS }}

  outdated-check:
    desc: Check outdated deps versions
    cmds:
      - clojure -M:outdated {{ .CLI_ARGS }}
  ...
```

### Итоги

Мне очень нравится подход и простота, которые предоставляет Kamal для развертывания. Он прозрачен и позволяет изменять почти любую конфигурацию сервисов. Однако было бы лучше иметь один бинарник вместо установки через Ruby. Также я бы избегал SSH-соединения с CI-воркера на сервер, но это, вероятно, разумный компромисс, учитывая простоту настройки.

Возможные улучшения общей установки приложения, которые выходят за рамки этой статьи:
- Периодическое резервное копирование базы данных (например, с использованием [`postgres-backup-s3`](https://github.com/eeshugerman/postgres-backup-s3?ref=luizkowalski.net) или аналогичного).
- CDN для статических файлов.
- Непривилегированный пользователь в [контейнере](https://kamal-deploy.org/docs/configuration/ssh/#using-a-different-ssh-user-than-root).
- Сбор метрик и логов.
- Использование базы данных как сервиса вместо запуска собственной.

Объем этой статьи немного шире, чем я изначально планировал, и я, вероятно, кратко рассмотрел некоторые важные части или вовсе не упомянул их. Я постарался сохранить баланс между отсутствием слишком большого количества деталей и передачей идеи процесса развертывания, сосредоточив внимание на последнем. В любом случае, вы всегда можете ознакомиться с примером [репозитория](https://github.com/abogoyavlensky/clojure-kamal-example) для получения большей ясности. В целом, я рад поделиться полным решением для настройки и запуска полнофункционального приложения на Clojure. Надеюсь, это будет полезно и использовано в таком виде или хотя бы послужит вдохновением для вашей собственной настройки!
