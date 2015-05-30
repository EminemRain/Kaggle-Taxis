import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import sys
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.mplot3d import Axes3D
import math

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
a_time = []
a_y = []
b_time = []
b_y = []
c_time = []
c_y = []
i = 0

angleBuckets = np.zeros((24), np.int)
bucketList = []

hourList = []



for line in outputData:
    i+=1
    if i == 1:
        continue

    line = line.split(",")
    date = dt.datetime.fromtimestamp(float(line[1]))
    h = date.hour
    # Account for UTC - Portugal difference
    #h = (h-11) % 24

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

    # add hour to the list
    hourList.append(date.hour)




# the random data
x = bucketList
y = hourList


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
hist, xedges, yedges = np.histogram2d(x, y, bins=24)

elements = (len(xedges) - 1) * (len(yedges) - 1)
xpos, ypos = np.meshgrid(xedges[:-1]+0.25, yedges[:-1]+0.25)

xpos = xpos.flatten()
ypos = ypos.flatten()
zpos = np.zeros(elements)
dx = 0.5 * np.ones_like(zpos)
dy = dx.copy()
dz = hist.flatten()

ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color='b', zsort='average')

plt.show()