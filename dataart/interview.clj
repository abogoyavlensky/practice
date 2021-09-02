(ns interview
  (:import [java.text SimpleDateFormat]
           [java.util Date]))


(defn moving-average [values period]
  (loop [values values
         period period
         acc []]
    (let [first (take period values)]
      (if (= (count first) period)
        (recur (rest values) period (conj acc (/ (reduce + first) period)))
        acc))))


(defn moving-average-lazy
  [values period]
  (let [average (fn [part]
                  (/ (reduce + part) period))]
    (->> values
      (partition period 1)
      (map average))))


(= [1.5 3.0 6.0 9.0]
   (moving-average-lazy '(1.0, 2.0, 4.0, 8.0, 10.0) 2))


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defn my-func
  [[a b] & {:keys [arg1 arg2] :or [:arg1 "default-1"]}]
  [[b a] arg1 arg2])


(let [a (Math/random), b (Math/random)]
  (= [[b a] "default-1" "default-2"]
     (my-func [a b])))

(= [[:b :a] "value-1" "value-2"]
   (my-func [:a :b] :arg1 "value-1" :arg2 "value-2"))

(= [[:y :x] "value-1" "default-2"]
   (my-func [:x :y] :arg1 "value-1"))

(= [[:bar :foo] "default-1" "value-2"]
   (my-func [:foo :bar] :arg2 "value-2"))

;;;;;;;;;;;;;;;;;;;;;;;;


(def request
  {:header {}
   :body   {:campaign "campaign-one"}})


(def campaigns (atom {"campaign-one" {"111-222-333-33" 8 "111-222-333-34" 4 "111-222-333-35" 6}
                      "campaign-two" {"111-222-444-01" 8 "111-222-444-02" 4 "111-222-444-03" 6}}))


(POST "/campaign" request
  (let [campaign-name     (get-in request [:body :campaign])
        available-numbers (get @campaigns campaign-name)
        number            (send-sms! available-numbers)]
    (swap! campaigns update-in [campaign-name number] inc)
    {:status 200}))



(comment
  (let [date (Date.)
        result (moving-average-lazy '(1.0, 2.0, 4.0, 8.0, 10.0) 2)]
    ;(.format (SimpleDateFormat. "MM/dd/yyyy") date)))
    (take 2 result)))
