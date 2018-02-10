from __future__ import division
from collections import defaultdict
from math import log
import csv


class NaiveBayesClassifier:
    def __init__(self, alpha = 1):
        self.alpha = alpha

    def fit(self, X, y):
        classes, freq = defaultdict(lambda: 0), defaultdict(lambda: 0)
        for feats, label in zip(X, y):
            classes[label] += 1  # count classes frequencies
            for feat in feats.split(" "):
                freq[label, feat] += 1  # count features frequencies

        for label, feat in freq:  # normalize features frequencies
            freq[label, feat] /= classes[label]
        for c in classes:  # normalize classes frequencies
            classes[c] /= len(y)
        self.classifier = classes, freq  # return P(C) and P(O|C)

    def predict(self, X):
        classes, prob = self.classifier
        return min(classes.keys(),  # calculate argmin(-log(C|O))
                   key=lambda cl: -log(classes[cl]) + \
                                  sum(-log(prob.get((cl, feat), 10 ** (-7))) for feat in X))

    def score(self, X_test, y_test):
        score = 0
        for current_X, current_Y in zip(X_test, y_test):
            if (self.predict(current_X) == current_Y):
                score += 1
        score /= len(X_test)
        return score

    def fitwithcollection(self):
        import csv
        with open("SMSSpamCollection") as f:
            data = list(csv.reader(f, delimiter="\t"))
        len(data)
        import string
        def clean(s):
            translator = str.maketrans("", "", string.punctuation)
            return s.translate(translator)
        X, y = [], []

        for target, msg in data:
            X.append(msg)
            y.append(target)
        X = [clean(x).lower() for x in X]
        X_train, y_train, X_test, y_test = X[:3900], y[:3900], X[3900:], y[3900:]
        self.fit(X_train, y_train)