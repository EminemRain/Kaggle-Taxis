import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import datetime as dt
import sys

name = sys.argv[1]
f = open(name,'r')

# Only cluster for 0th hour.
TIME = 3

x = []
y = []
for line in f:
    if not '1' in line:
        continue   

    data = line.split(",")

    if len(data) < 11:
        continue

    date = dt.datetime.fromtimestamp(float(data[5].replace("\"","")))
    h = date.hour

    #if h != TIME:
    #	continue
    index = len(data)
    x.append(float(data[index - 2].replace("\"","").replace("[","")) + 8)
    y.append(float(data[index - 1].replace("\"","").replace("]","")) - 41)


    # end coordinates - 5,6
    #index = len(data)
    #string += data[index-2] + ","
    #string += data[index-1] + "\n"

    #string = string.replace("]", "")
    #string = string.replace("[", "")
    #string = string.replace("\"", "")

    #outputData.append(string)

# the random data
fig, axScatter = plt.subplots(figsize=(8,8))

# the scatter plot:
axScatter.scatter(x, y)
axScatter.set_aspect(1.)

# create new axes on the right and on the top of the current axes
# The first argument of the new_vertical(new_horizontal) method is
# the height (width) of the axes to be created in inches.
divider = make_axes_locatable(axScatter)
axHistx = divider.append_axes("top", 1.2, pad=0.1, sharex=axScatter)
axHisty = divider.append_axes("right", 1.2, pad=0.1, sharey=axScatter)

# make some labels invisible
plt.setp(axHistx.get_xticklabels() + axHisty.get_yticklabels(),
         visible=False)

# now determine nice limits by hand:
binwidth = 0.25 # 0.25
xymax = np.max( [np.max(np.fabs(x)), np.max(np.fabs(y))] )
lim = ( int(xymax/binwidth) + 1) * binwidth

print xymax
print lim
print np.max(np.fabs(y))
print np.max(np.fabs(x))

bins = np.arange(-lim, lim + binwidth, binwidth)
axHistx.hist(x, bins=bins)
axHisty.hist(y, bins=bins, orientation='horizontal')

# the xaxis of axHistx and yaxis of axHisty are shared with axScatter,
# thus there is no need to manually adjust the xlim and ylim of these
# axis.

#axHistx.axis["bottom"].major_ticklabels.set_visible(False)
for tl in axHistx.get_xticklabels():
    tl.set_visible(False)
axHistx.set_yticks([0, 25, 50])

#axHisty.axis["left"].major_ticklabels.set_visible(False)
for tl in axHisty.get_yticklabels():
    tl.set_visible(False)
axHisty.set_xticks([0, 25, 50])

plt.title("Start distribution for hour " + str(TIME))
plt.draw()
plt.show()
plt.savefig('CoordHist' + str(TIME) + '.png')