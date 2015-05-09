import matplotlib.pyplot as plt
import sys

# get and open file
name = sys.argv[1]
f = open(name,'r')

# get data from file
a_size = 0
b_size = 0
c_size = 0
for line in f:
	if 'A' in line:
		a_size += 1
	elif 'B' in line:
		b_size += 1
	elif 'C' in line:
		c_size += 1





# The slices will be ordered and plotted counter-clockwise.
labels = 'Type A day', 'Type B Day', 'Type C Day'
sizes = [a_size, b_size, c_size]
colors = ['yellowgreen', 'gold', 'lightskyblue']

plt.pie(sizes, explode=(0, 0, 0), labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True)
# Set aspect ratio to be equal so that pie is drawn as a circle.
plt.axis('equal')

plt.show()