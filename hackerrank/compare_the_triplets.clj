(ns compare-the-triplets)


(comment
  (let [a-arg [17 28 30]
        b-arg [99 16 8]
        result (->> (zipmap a-arg b-arg)
                    (vec)
                    (reduce
                      (fn [acc n]
                        (let [a (first n)
                              b (second n)]
                          (cond
                            (> a b) (update acc :a inc)
                            (< a b) (update acc :b inc)
                            :else acc)))
                      {:a 0 :b 0}))]
    [(:a result) (:b result)]))
