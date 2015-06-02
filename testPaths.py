from sklearn.neighbors import NearestNeighbors
from math import *
import numpy as np
import sys
import utils
import string
import time

def finalDest(id, path, ids, paths):
    minFrechetDist = 999999999
    finalPoint = None
    i = 0
    for i in xrange(0, len(ids)):
        if ids[i] == id:
            continue
        p2 = utils.array_to_path(paths[i])
        if not p2:
            continue
        temp_p2 = utils.truncate_path(path, p2)
        if temp_p2 is None:
            continue

        # Compute Frechet distance between given path and each path in train file
        fDist = utils.frechet_dist(path, temp_p2)
        if (fDist < minFrechetDist):
            minFrechetDist = fDist
            finalPoint = p2[-1]
    return finalPoint

def naiveFrechetPredictor():
    # Predicts final points based on smallest frechet distance for each path in test.csv
    f = open(utils.kTestInputFile, "r")
    g = open(utils.kAnswerInputFile, "r")
    h = open(utils.kInputFile, "r")
    paths = []
    complete_path = []
    ids = []

    sys.setrecursionlimit(10000)

    i = 0
    for line in h:
        if i % 100000 == 0:
            print i
        i += 1
        path = utils.get_column(8, line)
        if not path:
            continue
        ids.append(utils.get_column(0, line))
        paths.append([path[0][0], path[0][1]])
        complete_path.append(utils.path_to_array(path))
    arr = np.array(paths, dtype="f")
    nbrs = NearestNeighbors(n_neighbors=10000, algorithm="ball_tree", metric=utils.distance_first).fit(arr)

    for line in f:
        ans = g.readline()
        ans = string.split(ans, ",")
        ans = (float(ans[1]), float(ans[2]))
        final_path = []
        final_ids = []
        for point in nbrs.kneighbors([ans], return_distance=False)[0]:
            final_path.append(complete_path[point])
            final_ids.append(ids[point])
        p = utils.get_column(utils.Columns.path, line)
        if not p:
            continue
        dest = finalDest(utils.get_column(0, line), p, final_ids, final_path)
        print utils.distance(dest, ans)

if __name__ == "__main__":
    naiveFrechetPredictor()
