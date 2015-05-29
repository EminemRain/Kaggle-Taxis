import utils
import numpy as np
import matplotlib as mlab
import matplotlib.pyplot as plt
import math

def main():
    data = []
    f = open(utils.kInputFile, "r")
    for line in f:
        path = utils.get_column(utils.Columns.path, line)
        if not path:
            continue
        data.append(utils.distance(path[0], path[-1]))

    binwidth = 1
    bins=range(int(math.floor(min(data))), int(math.ceil(
         max(data) + binwidth)), binwidth)
    # the histogram of the data
    plt.hist(data, bins=bins, facecolor='green', alpha=0.75)
    plt.xlabel('Trip Distance')
    plt.ylabel('Number of trips')
    plt.title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$')
    plt.axis([0, 20, 0, 1000000])
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
