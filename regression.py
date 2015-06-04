
import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeRegressor

# Create a random dataset
xData = np.genfromtxt('coords2.txt', delimiter=',', skiprows=1, dtype=None)
yData = np.genfromtxt('coords3.txt', delimiter=',', skiprows=1, dtype=None)
# Fit regression model
clf_1 = DecisionTreeRegressor(max_depth=20)
clf_2 = DecisionTreeRegressor(max_depth=5)
clf_3 = DecisionTreeRegressor(max_depth=8)
clf_1.fit(xData, yData)
clf_2.fit(xData, yData)
clf_3.fit(xData, yData)

# Predict
xTest = np.genfromtxt('testcoords2.txt', delimiter=',', skiprows=1, dtype=None)

y_1 = clf_1.predict(xTest)
y_2 = clf_2.predict(xTest)
y_3 = clf_3.predict(xTest)

# Plot the results
plt.figure()
plt.scatter(yData[:, 0], yData[:, 1], c="k", label="data")
plt.scatter(y_1[:, 0], y_1[:, 1], c="g", label="max_depth=20")
plt.scatter(y_2[:, 0], y_2[:, 1], c="r", label="max_depth=5")
plt.scatter(y_3[:, 0], y_3[:, 1], c="b", label="max_depth=8")
plt.xlim([-10, -6])
plt.ylim([43, 40])
plt.xlabel("data")
plt.ylabel("target")
plt.title("Multi-output Decision Tree Regression")
plt.legend()
#plt.show()

# output to later use to check distances to correct answers. This is just all the coordinates
for i in y_1:
	print str(i[0]) + "," + str(i[1])