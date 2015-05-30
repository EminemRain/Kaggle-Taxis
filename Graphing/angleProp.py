import matplotlib.pyplot as plt
import sys
import math
import numpy as np


name = sys.argv[1]
f = open(name,'r')

outputData = []
for line in f:
    if not '1' in line:
        continue   

    data = line.split(",")

    if len(data) < 11:
        continue

    string = ""

    # Call type - 0
    string += data[1] + ","

    # time - 1
    string += data[5] + ","

    # day type - 2
    string += data[6] + ","

    # start coordinates - 3,4
    string += data[8] + ","
    string += data[9] + ","

    # end coordinates - 5,6
    index = len(data)
    string += data[index-2] + ","
    string += data[index-1] + "\n"

    string = string.replace("]", "")
    string = string.replace("[", "")
    string = string.replace("\"", "")

    outputData.append(string)
    


# get data from file
a_hours = np.zeros((24), np.int)
b_hours = np.zeros((24), np.int)
c_hours = np.zeros((24), np.int)
i = 0

angleBuckets = np.zeros((24), np.int)
bucketList = []

hourList = []

for line in outputData:
    i+=1
    if i == 1:
        continue

    line = line.split(",")

    # Compute the angle and find the closest multiple of 30
    xDiff = float(line[5]) - float(line[3])
    yDiff = float(line[6]) - float(line[4])

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
    angleBuckets[bucket] += 1
    bucketList.append(bucket)


buckets = []
colors = []
explode = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
for i in range(0,24):
    buckets.append(str(i*15) + " - " + str((i+1)*15))
    colors.append('gold')
y_pos = np.arange(len(buckets))
performance = angleBuckets



# The slices will be ordered and plotted counter-clockwise.

plt.pie(angleBuckets, explode=explode, labels=buckets, colors=colors,
        autopct='%1.1f%%', shadow=True)
# Set aspect ratio to be equal so that pie is drawn as a circle.
plt.axis('equal')

plt.show()