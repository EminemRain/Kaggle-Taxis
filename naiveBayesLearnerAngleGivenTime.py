"""
Empirically get the conditonal probabilties of each vector angle given the hour, from a random subset of 500 000.
Using these stored probabilties, predict the angle given the hour. 
So P(Angle|hour) = % of angle at that hour. The way we'll do this is generate a random number, and then 
scale it up to 100. 
Take each percentage at a time, highest to lowest. If the random number is <= to it, done. If not, subtract 
that from the value, keep going. Whichever bucket we land in is the chosen angle. 
Then, from the training example, another random 300 000 say, compute the actual angle bucket. 
Compare, and see how many this gets wrong. If too many, then get the probabilities from this, and average them,
try again. That's how it can learn. 
"""


import numpy as np
import datetime as dt
import sys
import math

name = sys.argv[1]
f = open(name,'r')

outputData = []
totalPoints = 0
for line in f: 
    if not '1' in line:
        continue

    data = line.split(",")

    if len(data) < 11:
        continue

    string = ""

    # time - 0
    string += data[5] + ","

    # start coordinates - 1,2
    string += data[8] + ","
    string += data[9] + ","

    # end coordinates - 3,4
    index = len(data)
    string += data[index-2] + ","
    string += data[index-1] + "\n"

    string = string.replace("]", "")
    string = string.replace("[", "")
    string = string.replace("\"", "")

    outputData.append(string)
    

angleBuckets = np.zeros((24), np.int)
timeList = []
for l in angleBuckets:
    timeList.append(np.zeros((24), np.int))

for line in outputData:

    totalPoints += 1
    line = line.split(",")
    date = dt.datetime.fromtimestamp(float(line[0]))
    h = date.hour
    # Account for UTC - Portugal difference. IS THIS RELEVANT?
    #h = (h-11) % 24

    # Compute the angle and find the closest multiple of 30
    xDiff = float(line[3]) - float(line[1])
    yDiff = float(line[4]) - float(line[2])

    angle = 0
    if xDiff == 0:
        angle = math.pi/2
    else:
        angle = np.arctan(abs(yDiff/xDiff))

    # Decide on quadrant
    if xDiff < 0 and yDiff >=0: # second quadrant. Add pi/2
        angle += math.pi/2.0
    elif xDiff < 0 and yDiff < 0: # 3rd quadrant. Add pi
        angle += math.pi
    elif xDiff >= 0 and yDiff < 0: # 4th quadrant. 2pi - angle 
        angle = 2*math.pi - angle

    # Compute bucket, add to list
    bucket = math.floor(angle/(math.pi/12))
    #angleBuckets[bucket] += 1

    # add hour to the list
    #hourList.append(date.hour)

    timeList[date.hour][bucket] += 1 

# Compute conditional probabilties
string = ""
for hour in timeList: # For each hour
    #print "Hour: " + str(hour)
    # Get the percentage of each angle bucket for that hour
    numList = []
    total = 0
    for angleBucket in hour:
        total += angleBucket
        numList.append(angleBucket)
    stringList = []
    if total != 0:
        for l in numList:
            stringList.append(str(float(100*l)/float(total)) + ",")
    stringList.append(str(total) + "\n")
    #print "NumList: " + str(numList)
    #print "StringList: " + str(stringList)
    string += "".join(stringList)
    #print "String: " + string 

with open('nbAnglefromTime.txt', "w") as output_file:
        output_file.write(string)


