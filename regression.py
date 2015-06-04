import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeRegressor
import utils
import string
from sklearn import cross_validation
from sklearn.ensemble import AdaBoostRegressor

def main():
    features = []
    classes = []
    ids = []
    tests = []
    f = open(utils.kRegressionTrainFile, "r")
    for line in f:
        r = string.split(line, ",")
        features.append([int(r[i]) for i in xrange(0, 4)] + [float(r[i]) for i in xrange(4, 8)])
        classes.append([float(r[8]),float(r[9])])
    test_regression(features, classes)
    
    f = open(utils.kRegressionTestFile, "r")
    for line in f:
        r = string.split(line, ",")
        ids.append(int(r[0]))
        tests.append([int(r[i]) for i in xrange(1, 5)] + [float(r[i]) for i in xrange(5, 9)])
        
    generate_results(features, classes, ids, tests)

def generate_results(features, classes, ids, test_input):
    classes0 = []
    classes1 = []
    for cls in classes:
        classes0.append(cls[0])
        classes1.append(cls[1])
    clf0 = AdaBoostRegressor(DecisionTreeRegressor(max_depth=20), n_estimators=5)
    clf1 = AdaBoostRegressor(DecisionTreeRegressor(max_depth=20), n_estimators=5)
    clf0.fit(features, classes0)
    clf1.fit(features, classes1)
    res_dict = {}
    for i in xrange(len(ids)):
        p0 = clf0.predict(test_input[i])[0]
        p1 = clf1.predict(test_input[i])[0]
        res_dict[ids[i]] = (p1, p0)

    utils.create_submission(res_dict)

def test_regression(features, classes):
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(features,
                                       classes, test_size=0.1, random_state=0)

    clf_10 = AdaBoostRegressor(DecisionTreeRegressor(max_depth=20), n_estimators=10)
    clf_11 = AdaBoostRegressor(DecisionTreeRegressor(max_depth=20), n_estimators=10)
    clf_2 = DecisionTreeRegressor(max_depth=20)

    y_train0 = []
    y_train1 = []
    for y in y_train:
        y_train0.append(y[0])
        y_train1.append(y[1])

    print "fitting 1 part 1"
    clf_10.fit(X_train, y_train0)
    print "fitting 1 part 2"
    clf_11.fit(X_train, y_train1)
    print "fitting 2"
    clf_2.fit(X_train, y_train)

    l1 = []
    l2 = []
    print "testing"
    for i in xrange(len(X_test)):
        pred10 = clf_10.predict(X_test[i])
        pred11 = clf_11.predict(X_test[i])
        pred2 = clf_2.predict(X_test[i])
        l1.append(utils.distance((pred10[0], pred11[0]), y_test[i]))
        l2.append(utils.distance(pred2[0], y_test[i]))

    print sum(l1) / len(l1)
    print sum(l2) / len(l2)

main()
