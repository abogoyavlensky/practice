(ns mini_max_sum)


(defn output
  [result]
  (->> result
       (clojure.string/join "\n")
       (spit (get (System/getenv) "OUTPUT_PATH" *out*))))


(defn mini-max-sum
  []
  ())


(comment
  (let [numbers [1 5 3 4 2]]
    ()))
