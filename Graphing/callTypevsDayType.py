import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import sys

# get and open file
name = sys.argv[1]
f = open(name,'r')



# get data from file
aa_size = 0
ab_size = 0
ac_size = 0
ba_size = 0
bb_size = 0
bc_size = 0
ca_size = 0
cb_size = 0
cc_size = 0
for line in f:
	if 'A,A' in line:
		aa_size += 1
	elif 'A,B' in line:
		ab_size += 1
	elif 'A,C' in line:
		ac_size += 1
	elif 'B,A' in line:
		ba_size += 1
	elif 'B,B' in line:
		bb_size += 1
	elif 'B,C' in line:
		bc_size += 1
	elif 'C,A' in line:
		ca_size += 1
	elif 'C,B' in line:
		cb_size += 1
	elif 'C,C' in line:
		cc_size += 1


# Example data
types = ('Trip A Day A', 'Trip A Day B', 'Trip A Day C', 'Trip B Day A', 'Trip B Day B', 'Trip B Day C', 'Trip C Day A', 'Trip C Day B', 'Trip C Day C')
y_pos = np.arange(len(types))
performance = (aa_size, ab_size, ac_size, ba_size, bb_size, bc_size, ca_size, cb_size, cc_size)
error = 0

plt.barh(y_pos, performance, xerr=error, align='center', alpha=0.4)
plt.yticks(y_pos, types)
plt.xlabel('Amount')
plt.title('Amounts of types of trips and days')

plt.show()