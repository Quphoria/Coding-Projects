from P_4 import *

#Generate a sequence of numbers from -10 to 10 with 100 steps in between
x = np.linspace(-10, 10, 100)
#Create a second array using sine
y = np.sin(x)
#The plot function makes a line chart of one array against another
plt.plot(x, y, marker="x")
plt.show()
input()
