(ns diagonal_difference)

(defn calc-diagonals
  [acc [i v]]
  (-> acc
      (update 0 + (get v i))
      (update 1 + (get v (- (count v) (inc i))))))

(defn diagonal-difference
  [matrix]
  (->> (map-indexed vector matrix)
       (reduce calc-diagonals [0 0])
       (apply -)
       (Math/abs)))

(comment
  (let [matrix [[11 2 4]
                [4 5 6]
                [10 8 -12]]]
    (diagonal-difference matrix)))
