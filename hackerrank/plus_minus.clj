(ns plus_minus
  (:require [clojure.string]))

(defn calc
  [acc number]
  (cond
    (< number 0) (update acc :neg inc)
    (> number 0) (update acc :pos inc)
    :else (update acc :zero inc)))

(defn plus-minus
  [numbers]
  (let [total (count numbers)
        counts (reduce calc {:pos 0
                             :neg 0
                             :zero 0} numbers)]
    (clojure.string/join "\n"
                         (map #(float (/ (get counts %) total)) [:pos :neg :zero]))))

(comment
  (let [numbers [-1 -2 0 1 3]]
    (plus-minus numbers)))
