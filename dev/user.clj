(ns user
  (:require [clojure.tools.namespace.repl :as repl]
            [clojure.test :as test]
            [hashp.core]))

(repl/set-refresh-dirs "hackerrank" "interview")

(defn reset
  "Reload changed namespaces."
  []
  (repl/refresh))


(defn run-all-tests
  "Reload changed namespaces."
  []
  (reset)
  (test/run-all-tests #"tuna.*-test"))
