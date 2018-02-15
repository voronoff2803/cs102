x = ["a a a","a b a","b b a","c c c"]
y = ["ham","spam","spam","spam"]


def fit(X, y):
    classes, freq = {}, {}
    for feats, label in zip(X, y):
        classes[label] = 0
        for feat in feats.split(" "):
            freq[(label, feat)] = 0
    for feats, label in zip(X, y):
        classes[label] += 1  # count classes frequencies
        for feat in feats.split(" "):
            freq[(label, feat)] += 1  # count features frequencies

    for label, feat in freq:  # normalize features frequencies
        freq[(label, feat)] /= classes[label]
    for c in classes:  # normalize classes frequencies
        classes[c] /= len(y)
    classifier = classes, freq  # return P(C) and P(O|C)
    print(classifier)
    return classifier

def predict(X):
    pred = {}
    classes, prob = fit(x, y)
    for key in classes.keys():
        pred[key] = 1
    for key in classes.keys():
        for word in X.split(" "):
            try:
                pred[key] *= prob[(key,word)]
            except:
                pass
    b = []

    for i in pred.keys():
        b.append(pred[i])
    for i in pred.keys():
        if pred[i] == max(b):
            return i
    return None

print(predict("c"))

