import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import sys
from pytz.reference import Eastern

# get and open file
name = sys.argv[1]
f = open(name,'r')



# get data from file
a_time = []
a_y = []
b_time = []
b_y = []
c_time = []
c_y = []
i = 0

a_hours = np.zeros((24), np.int)
b_hours = np.zeros((24), np.int)
c_hours = np.zeros((24), np.int)

for line in f:
	i+=1
	if i == 1:
		continue

	line = line.split(",")
	date = dt.datetime.fromtimestamp(float(line[1]))
	h = date.hour
	# Account for UTC - Portugal difference
	#h = (h-11) % 24

	if 'A' in line[0]:
		a_time.append(date.hour)
		a_y.append(1)
		a_hours[h] += 1
	elif 'B' in line[0]:
		b_time.append(date.hour)
		b_y.append(2)
		a_hours[h] += 1
	elif 'C' in line[0]:
		c_time.append(date.hour)
		c_y.append(3)
		a_hours[h] += 1

print "Number of A's: " + str(len(a_time))
print "Number of B's: " + str(len(b_time))
print "Number of C's: " + str(len(c_time))


hours = []
for i in range(0,24):
	hours.append(str(i))
y_pos = np.arange(len(hours))
performance = a_hours
error = 0

plt.barh(y_pos, performance, xerr=error, align='center', alpha=0.4)
plt.yticks(y_pos, hours)
plt.xlabel('number of trips at hour')
plt.title('Distribution of total trips throughout day with Timezone')

plt.show()