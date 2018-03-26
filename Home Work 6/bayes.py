from __future__ import division
import math


class NaiveBayesClassifier:
    def __init__(self, alpha = 0.55):
        self.alpha = alpha

    def fit(self, X, y):
        classes, freq = {}, {}
        allwords = []
        labels = set(y)
        for words in X:
            for word in words.split(" "):
                allwords.append(word)
                for label in labels:
                    classes[label] = 0
                    freq[(label,word)] = self.alpha # Может это альфа хз
        for feats, label in zip(X, y):  # Нужно разобраться вычислять вероятность по словам или по предложениям. Мне кажется по словам лучше
            for feat in feats.split(" "):
                classes[label] += self.alpha
                freq[(label, feat)] += self.alpha
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
                    pred[key] += math.log (prob[(key, word)])
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

x = ["i love this sandwich","this is an amazing place","i feel very good about these beers","this is my best work","what an awesome view","i do not like this restaurant","i am tired of this stuff","i can’t deal with this","he is my sworn enemy","my boss is horrible"]
y = ["Positive","Positive","Positive","Positive","Positive","Negative","Negative","Negative","Negative","Negative"]

ba = NaiveBayesClassifier()
ba.fit(X_train, y_train)
print(ba.classifier)
print(ba.score(X_test,y_test))

