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

NOW TEST. This takes in a series of points, and for each point, it gets the hour and the true angle. 
It then, given the hour, predicts the angle that the taxi should travel in relative to start position. 
"""


import numpy as np
import datetime as dt
import sys
import math
import random

name = sys.argv[1]
testInput = open(name,'r')

name = sys.argv[2]
data = open(name,'r')

# grab data
hourBuckets = []
for line in data:
    line = line.split(",")
    hourBuckets.append(line)

# test each point
numCorrect = 0
numIncorrect = 0
for line in testInput: 
    if not '1' in line:
        continue

    # Get time and points from line
    data = line.split(",")

    if len(data) < 11: # line doesn't have an end vector - ignore it
        continue
    # time - 0
    hour = int(data[5].replace("\"",""))
    # start coordinates - 1,2
    x1 = float(data[8].replace("\"","").replace("[",""))
    y1 = float(data[9].replace("\"","").replace("]",""))
    index = len(data)
    x2 = float(data[index-2].replace("\"","").replace("[",""))
    y2 = float(data[index-1].replace("\"","").replace("]",""))

    # Compute the angle and find the closest multiple of 15
    xDiff = x2 - x1
    yDiff = y2- y1

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

    # Get the hour
    date = dt.datetime.fromtimestamp(float(hour))
    h = date.hour

    # generate random number, get predicted angle
    # The order of subtraction actually will affect it
    random.seed()
    num = np.random.rand()*100 # random number from 0 to 100
    #print num
    for i in range(0,24):  
        #print hourBuckets[h][i] 
        if num < float(hourBuckets[h][i]):
            num = math.floor(num)
            #print "Bucket " + str(i)
            break
        else:
            num -= float(hourBuckets[h][i])
    #print i

    # Predicted angle
    predAngleBucket = i
    trueAngle = angle*180/math.pi
    print "Predicted the angle bucket " + str(predAngleBucket*15) + " - " + str(predAngleBucket*15 + 15) + " given the hour " + str(h)
    print "Actual angle is " + str(trueAngle)
    if predAngleBucket*15 < trueAngle and trueAngle < (predAngleBucket*15 + 15):
        numCorrect += 1
    else:
        numIncorrect += 1
    print ""
    #num = angle/(math.pi/12)

print "Correct Guesses: " + str(numCorrect)
print "Incorrect Guesses: " + str(numIncorrect)
