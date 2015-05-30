from math import *
import numpy as np
import sys
import utils


def finalDest(path):
    minFrechetDist = 999999999
    finalPoint = None
    f = open(utils.kInputFile, "r")
    for line in f:
        p2 = utils.get_column(utils.Columns.path, line)
        if not p2:
            continue
        
        if len(p2) < len(path):
            continue


        # Compute Frechet distance between given path and each path in train file
        fDist = utils.frechet_dist(path, p2[:len(path)])
        if (fDist < minFrechetDist):
            minFrechetDist = fDist
            finalPoint = p2[-1]

    return finalPoint

def naiveFrechetPredictor():
    # Predicts final points based on smallest frechet distance for each path in test.csv
    f = open(utils.testInputFile, "r")

    for line in f:
        p = utils.get_column(utils.Columns.path, line)
        if not p:
            continue
        finalDest(p)

