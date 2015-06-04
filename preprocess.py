import utils
from random import randint

f = open("train.csv", "r")

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
    print "%s,%s,%s,%s,%f,%f,%f,%f,%f,%f" % (origin_call, origin_stand, taxi_id, 
                                                timestamp, path[0][0],path[0][1],point[0],
                                                point[1],path[-1][0],path[-1][1])