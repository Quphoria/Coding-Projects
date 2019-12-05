import math
import numpy as np

resolution = 200

vector = np.array([1.,0.,0.])
vectors = np.zeros([resolution,3])

pi_unit = math.pi / (resolution/2)
for i in range(int(resolution/2)):
    angle = pi_unit * i
    vectors[i][0] = math.cos(angle)
    vectors[i][1] = math.sin(angle)
for i in range(int(resolution/2)):
    angle = -pi_unit * i
    vectors[resolution-i-1][0] = math.cos(angle)
    vectors[resolution-i-1][1] = math.sin(angle)

view_angle = 1 * math.pi
min_cos = math.cos(view_angle/2)

dp = np.dot(vectors,vector)
indices = np.nonzero((min_cos<=dp))
print(vectors[indices])