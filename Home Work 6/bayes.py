from __future__ import division
from collections import defaultdict
from math import log


class NaiveBayesClassifier:
    def __init__(self, alpha = 1):
        self.alpha = alpha

    def fit(self, X, y):
        classes, freq = defaultdict(lambda: 0), defaultdict(lambda: 0)
        for feats, label in zip(X, y):
            classes[label] += 1  # count classes frequencies
            for feat in feats:
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
        """ Returns the mean accuracy on the given test data and labels. """
        pass



Xx = [['aa', 'ba', 'ca'],['da', 'ea', 'fa']]
Yy = ['+','-']

aaa = NaiveBayesClassifier()
aaa.fit(Xx,Yy)
print(aaa.predict(['aa','ba']))