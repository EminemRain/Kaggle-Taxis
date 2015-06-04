import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeRegressor
import utils
import string
from sklearn import cross_validation

features = []
classes = []

f = open(utils.kRegressionTrainFile, "r")

for line in f:
    r = string.split(line, ",")
    features.append([int(r[i]) for i in xrange(0, 4)] + [float(r[i]) for i in xrange(4, 8)])
    classes.append([float(r[8]),float(r[9])])

X_train, X_test, y_train, y_test = cross_validation.train_test_split(features,
                                   classes, test_size=0.1, random_state=0)

clf_1 = DecisionTreeRegressor(max_depth=20)
clf_2 = DecisionTreeRegressor(max_depth=5)
clf_3 = DecisionTreeRegressor(max_depth=8)

print "fitting 1"
clf_1.fit(X_train, y_train)
print "fitting 2"
clf_2.fit(X_train, y_train)
print "fitting 3"
clf_3.fit(X_train, y_train)

l1 = []
l2 = []
l3 = []
print "testing"
count = 0
for i in xrange(len(X_test)):
    pred1 = clf_1.predict(X_test[i])
    pred2 = clf_2.predict(X_test[i])
    pred3 = clf_3.predict(X_test[i])
    l1.append(utils.distance(pred1[0], y_test[i]))
    l2.append(utils.distance(pred2[0], y_test[i]))
    l3.append(utils.distance(pred3[0], y_test[i]))
    count += 1
    if count == 0 % 2:
    	print pred3[0]
    	print y_test[i]
    	print X_test[i]


print sum(l1) / len(l1)
print sum(l2) / len(l2)
print sum(l3) / len(l3)
print count
