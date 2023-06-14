from enum import Enum


class ModelOptions(str, Enum):
  logisticRegression = "logisticRegression"
  knn = "knn"
  svm = "svm"
  naiveBayes = "naiveBayes"
  decisionTrees = "decisionTrees"
  linearRegression = "linearRegression"