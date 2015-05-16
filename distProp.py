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
i = 0

NUM_BUCKETS = 50.0
distBuckets = np.zeros((NUM_BUCKETS), np.int)

counter = 0

for line in outputData:
    i+=1
    if i == 1:
        continue

    line = line.split(",")

    # Compute the angle and find the closest multiple of 30
    xDiff = float(line[5]) - float(line[3])
    yDiff = float(line[6]) - float(line[4])
    dist = math.sqrt(xDiff**2 + yDiff**2)

    if dist > 0.1:
        continue

    counter += 1
    # Compute bucket, add to list
    bucket = math.floor(NUM_BUCKETS*10*dist)
    distBuckets[bucket] += 1

buckets = []
colors = []
explode = np.zeros(NUM_BUCKETS, np.int)
for i in range(0,int(NUM_BUCKETS)):
    buckets.append(str(i*(0.1/NUM_BUCKETS))  + " - " + str((i+1)*(0.1/NUM_BUCKETS)))
    colors.append('green')



# The slices will be ordered and plotted counter-clockwise.
print counter
plt.pie(distBuckets, explode=explode, labels=buckets, colors=colors,
        autopct='%1.1f%%', shadow=True)
# Set aspect ratio to be equal so that pie is drawn as a circle.
plt.axis('equal')
plt.title('Total distance distribution of ' + str(counter) + ' trips')

plt.show()

