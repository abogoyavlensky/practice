(ns arrival
  (:require [clojure.string :as str]))




(comment
 ; Есть дерево, у каждого элемента есть идентификатор, имя и дочерние элементы. Все это лежит в мапе по id.
 ; Нужно отфильтровать те элементы, имя которых содержит определенную подстроку.
 ; И оставить их и подветку предков, которые ведут к ним.
  (let [data {1 {:name "Foo"
                 :children [2 3]}
              2 {:name "Bar"
                 :children []}
              3 {:name "Baz"
                 :children [4]}
              4 {:name "xxx"
                 :children []}
              5 {:name "yyy"
                 :children []}}
        items (->> data
                  (reduce-kv (fn [m k v]
                               (if (str/includes? (:name v) "xxx")
                                 (assoc m k v)
                                 m)) {}))]
    (filter)))




  ;; ищем "xxx", хотим получить:
  ;#{{:id 1
  ;   :name "Foo"
  ;   :children [3]}
  ;  {:id 3
  ;   :name "Baz"
  ;   :children [4]}
  ;  {:id 4
  ;   :name "xxx"
  ;   :children []}})

;;;;;;;;;;;;;;;;;;;;;;;;;;




(defn do-transformation [items-vec]
  (let [ids (atom #{})]
    (reduce (fn [acc item]
              (if (true? (contains? @ids (:id item)))
                acc
                (do
                  (swap! ids conj (:id item))
                  (conj acc {:v (:value item)}))))
            []
            items-vec)))
