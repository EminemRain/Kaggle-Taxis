import utils
from random import randint
f = open("train.csv", "r")
out = open(utils.kRegressionTrainFile, "w")
for line in f:
    origin_call = utils.get_column(2, line)
    if origin_call is None:
        origin_call = 0
    origin_stand = utils.get_column(3, line)
    if origin_stand is None:
        origin_stand = 0
    taxi_id = utils.get_column(4, line)
    timestamp = utils.get_column(5, line)
    missing_data = utils.get_column(7, line)
    path = utils.get_column(8, line)
    if len(path) < 2 or missing_data:
        continue
    point = path[randint(1, len(path) - 1)]
    out.write("%s,%s,%s,%s,%f,%f,%f,%f,%f,%f\n" % (origin_call, origin_stand, taxi_id, 
                                                timestamp, path[0][0],path[0][1],point[0],
                                                point[1],path[-1][0],path[-1][1]))
f = open("test.csv", "r")
out = open(utils.kRegressionTestFile, "w")
for line in f:
    id = utils.get_column(0, line)
    origin_call = utils.get_column(2, line)
    if origin_call == "NA":
        origin_call = 0
    origin_stand = utils.get_column(3, line)
    if origin_stand == "NA":
        origin_stand = 0
    taxi_id = utils.get_column(4, line)
    timestamp = utils.get_column(5, line)
    missing_data = utils.get_column(7, line)
    path = utils.get_column(8, line)
    out.write("%s,%s,%s,%s,%s,%f,%f,%f,%f\n" % (id, origin_call, origin_stand, taxi_id, 
                                                timestamp, path[0][0],path[0][1],path[-1][0],path[-1][1]))
