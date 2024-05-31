(ns a_very_big_sum)

(comment
  (let [ar [1000000001 1000000002 1000000003 1000000004 1000000005]]
    (->> (map bigint ar)
         (reduce + (bigint 0)))))
