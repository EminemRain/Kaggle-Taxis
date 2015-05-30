from math import *
import re
import string
import datetime
import numpy as np
from memoize import mproperty

kInputFile = "train.csv"
testInputFile = "test.csv"

class Columns:
    trip_id = 0
    call_type = 1
    origin_call = 2
    origin_stand = 3
    taxi_id = 4
    timestamp = 5
    day_type = 6
    missing_data = 7
    path = 8

class DayType:
    normal_day = 0
    holiday = 1
    pre_holiday = 2

def distance(loc1, loc2):
    return distance_internal(loc1[0], loc1[1], loc2[0], loc2[1])

def createSubmission(d): # d is the dictionary where numerical keys map to tuples
    sub = "\"TRIP_ID\",\"LATITUDE\",\"LONGITUDE\"\n"

    for key in sorted(d):  
        coords = d[key]
        sub += "\"T" + str(key) + "\"," + str(coords[0]) + "," + str(coords[1]) + "\n"

    with open('submission.csv', "w") as output_file:
        output_file.write(sub)

def distance_internal(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def get_column(column, line):
    col = string.split(line, ",", 8)[column]
    col = re.sub("\"", "", col) 

    if col == "":
        return None
    if column == Columns.trip_id:
        return int(col)
    elif column == Columns.call_type:
        return col
    elif column == Columns.origin_call:
        return int(col)
    elif column == Columns.origin_stand:
        return int(col)
    elif column == Columns.taxi_id:
        return int(col)
    elif column == Columns.timestamp:
        return datetime.datetime.fromtimestamp(int(col))
    elif column == Columns.day_type:
        return col
    elif column == Columns.missing_data:
        return col == "True"
    elif column == Columns.path:
        coords = []
        for coord in string.split(col, "]"):
            regex = re.compile(r"\[([^[]*),([^[]*)") 
            matches = regex.search(coord)
            if matches == None:
                continue
            coords.append((float(matches.group(1)), float(matches.group(2))))
        return coords

def _c(ca,i,j,P,Q):
    if ca[i,j] > -1:
        return ca[i,j]
    elif i == 0 and j == 0:
        ca[i,j] = distance(P[0],Q[0])
    elif i > 0 and j == 0:
        ca[i,j] = max(_c(ca,i-1,0,P,Q),distance(P[i],Q[0]))
    elif i == 0 and j > 0:
        ca[i,j] = max(_c(ca,0,j-1,P,Q),distance(P[0],Q[j]))
    elif i > 0 and j > 0:
        ca[i,j] = max(min(_c(ca,i-1,j,P,Q),_c(ca,i-1,j-1,P,Q),_c(ca,i,j-1,P,Q)),distance(P[i],Q[j]))
    else:
        ca[i,j] = float("inf")
    return ca[i,j]

""" Computes the discrete frechet distance between two polygonal lines
Algorithm: http://www.kr.tuwien.ac.at/staff/eiter/et-archive/cdtr9464.pdf
P and Q are arrays of 2-element arrays (points)
"""
# TODO(karl): add source
def frechet_dist(P,Q):
    ca = np.ones((len(P),len(Q)))
    ca = np.multiply(ca,-1)
    return _c(ca,len(P)-1,len(Q)-1,P,Q)

