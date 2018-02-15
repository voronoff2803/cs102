from __future__ import division
import math


class NaiveBayesClassifier:
    def __init__(self, alpha = 1):
        self.alpha = alpha

    def fit(self, X, y):
        classes, freq = {}, {}
        allwords = []
        for words in X:
            for word in words.split(" "):
                allwords.append(word)
                for label in y:
                    classes[label] = 0
                    freq[(label,word)] = self.alpha
        for feats, label in zip(X, y):  # Нужно разобраться вычислять вероятность по словам или по предложениям. Мне кажется по словам лучше
            for feat in feats.split(" "):
                classes[label] += 1
                freq[(label, feat)] += 1
        count = len(set(allwords))
        for feat, item in freq.items():
            freq[feat] = item / (classes[feat[0]] + count)
        self.classifier = classes, freq

    def predict(self, X):
        pred = {}
        classes, prob = self.classifier
        for key in classes.keys():
            pred[key] = 0
        for key in classes.keys():
            for word in X.split(" "):
                try:
                    pred[key] += math.log(prob[(key, word)])
                except:
                    pass
        b = []
        for i in pred.keys():
            b.append(pred[i])
        for i in pred.keys():
            if pred[i] == max(b):
                return i
        return None

    def score(self, X_test, y_test):
        score = 0
        for current_X, current_Y in zip(X_test, y_test):
            if (self.predict(current_X) == current_Y):
                score += 1
        score /= len(X_test)
        return score