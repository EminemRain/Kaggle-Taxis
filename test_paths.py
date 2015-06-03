from math import *
import numpy as np
import os.path
from sklearn.neighbors import NearestNeighbors
import string
import sys
import time
import utils

def main():
    # Prevent crashing when recursing on a particularly long path.
    sys.setrecursionlimit(10000)
    
    try:
        training_data = open(utils.kTrainingInputFile, "r")
    except:
        print "No training data found, please provide a file called:",\
              utils.kTrainingInputFile
        sys.exit(-1)

    try:
        tests = open(utils.kTestInputFile, "r")
    except:
        print "No test data found, please provide a file called:",\
               utils.kTestInputFile
        sys.exit(-1)

    # The answers file is optional.
    try:
        answers = open(utils.kAnswerFile, "r")
    except:
        print "No answers file provided, won't print accuracy information.",\
               "To get information about algorithm accuracy please provide a",\
               "file called:", utils.kAnswerFile
        answers = None

    predict_destinations(training_data, tests, answers)

def frechet_predictor(test_id, test_path, train_infos):
    min_distance = 999999999
    destination = None
    for train_info in train_infos:
        if train_info[0] == test_id:
            print "Warning: You have matching ids within your test and training set."
            continue
        train_path = utils.array_to_path(train_info[1])
        if not train_path:
            continue
        truncated_train_path = utils.truncate_path(test_path, train_path)
        if truncated_train_path is None:
            continue

        # Compute Frechet distance between given path and each path in train file
        distance = utils.frechet_dist(truncated_train_path, test_path)
        if (distance < min_distance):
            min_distance = distance
            destination = train_path[-1]
    return destination

def predict_destinations(training_data, tests, answers):
    training_infos = get_training_infos(training_data)
    nearest_neighbors = create_nearest_neighbors_predictor(training_infos)

    for line in tests:
        nearest_paths = []
        test_id = utils.get_column(utils.Columns.trip_id, line)
        test_path = utils.get_column(utils.Columns.path, line)
        if not test_path:
            continue
        for index in nearest_neighbors.kneighbors([test_path[0]],
        return_distance=False)[0]:
            nearest_paths.append(training_infos[index])
        predicted_destination = frechet_predictor(test_id, test_path, nearest_paths)
        print test_id, "|", predicted_destination,
        if answers is not None:
            real_destination = get_real_destination(answers)
            print "|", utils.distance(real_destination, predicted_destination)
        else:
            print ""

def get_training_infos(training_data):
    training_infos = []
    i = 0
    for line in training_data:
        if i % 100000 == 0:
            print i
        i+=1
        id = utils.get_column(utils.Columns.trip_id, line)
        path = utils.get_column(utils.Columns.path, line)
        # Drop empty paths.
        if not path:
            continue
        training_infos.append((id, utils.path_to_array(path)))
    return training_infos

def create_nearest_neighbors_predictor(training_infos):
    path_starts = []
    for info in training_infos:
        path = info[1]
        path_starts.append([path[0], path[1]])
    return NearestNeighbors(n_neighbors=10000, algorithm="ball_tree",
           metric=utils.distance_first).fit(np.array(path_starts, dtype="f"))

def get_real_destination(answers):
    line = answers.readline()
    ans = string.split(line, ",")
    return (float(ans[1]), float(ans[2]))

if __name__ == "__main__":
    main()
