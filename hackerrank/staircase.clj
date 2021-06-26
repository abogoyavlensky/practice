(ns staircase)

(defn output
  [result]
  (->> result
       (clojure.string/join "\n")
       (spit (get (System/getenv) "OUTPUT_PATH" *out*))))


(defn staircase
  [total]
  (for [space-count (range (- total 1) -1 -1)
        :let [sign-count (- total space-count)
              spaces (clojure.string/join "" (repeat space-count " "))
              signs (clojure.string/join "" (repeat sign-count "#"))]]
    (str spaces signs)))


(comment
  (output (staircase 6)))
