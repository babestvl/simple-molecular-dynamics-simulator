import numpy as np
import math
import time
import datetime

start_time = time.time()

# Initial Values
count = 0
delta_time = 1 * math.pow(10, -12)
mass_argon = 39.948
mol = 6.022 * math.pow(10, 23)
sigma = 5.670 * math.pow(10, -8)
T = 300
R = 1
# wrong value
Kb = 1.38 * math.pow(10, -5)

# Initial Atoms Position
xp = np.random.uniform(-1, 1, 10000)
yp = np.random.uniform(-1, 1, 10000)
zp = np.random.uniform(-1, 1, 10000)

# Delete unusable atoms
delete_index = []
for i in range(10000):
  r = (xp[i]**2)+(yp[i]**2)+(zp[i]**2)
  r = r**(1/2)
  if r > R:
    delete_index.append(i)
    count += 1
xp = np.delete(xp, delete_index)
yp = np.delete(yp, delete_index)
zp = np.delete(zp, delete_index)
atom_range = len(xp)

# Random Velocity and Direction
xd = np.random.uniform(-5, 5, atom_range)
yd = np.random.uniform(-5, 5, atom_range)
zd = np.random.uniform(-5, 5, atom_range)
random_velocity = np.random.uniform(-5, 5, 3)

# Initial Velocity and Momentum
a = math.sqrt(random_velocity[0]**2 + random_velocity[1]**2 + random_velocity[2]**2)
initial_velocity = math.sqrt((3 * Kb * T)/(mass_argon))
velocity_vector = initial_velocity * (random_velocity / a)
momentum_vector = mass_argon * velocity_vector

# Apply Initial Velocity to Direction
for i in range(atom_range):
  xd[i] *= velocity_vector[0]
  yd[i] *= velocity_vector[1]
  zd[i] *= velocity_vector[2]

def update(x,y,z,i):
  global xd, yd, zd
  return (x+xd[i], y+yd[i], z+zd[i])

def verletCalculation(force):
  global delta_time, mass_argon
  momantum = momantum + 0.5 * delta_time * force
  r = r + delta_time * momantum / mass_argon
  force = forceCalculation(r)
  momantum = + 0.5 * delta_time * force
  return (momantum, r)

def forceCalulation(r):
  pass

result_file = open("fluid.xyz","w")

# -------------------------

for j in range(1000):
  result_file.write("{}\n{}\n".format(atom_range,1))
  for i in range(atom_range):
    if xp[i] != 0:
      result_file.write("{} {} {} {}\n".format("H", xp[i], yp[i], zp[i]))
      xp[i],yp[i],zp[i] = update(xp[i], yp[i], zp[i], i)
      
# -------------------------

result_file.close()

print("--- %s seconds ---" % (time.time() - start_time))
