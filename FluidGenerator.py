import numpy as np
import math
import time
import datetime

start_time = time.time()

# Initial Values
count = 0
delta_time = 1 * math.pow(10, -15) # 0.001 s to ps
mass_argon = 39.948
mol = 6.022 * math.pow(10, 23)
sigma = 5.670367 * math.pow(10, -8)
T = 300
R = 1
# wrong value
Kb = 2.292674407 * math.pow(10, -50)
Kb = 1.3806485279 * math.pow(10, -23)

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
xv = np.random.uniform(-5, 5, atom_range)
yv = np.random.uniform(-5, 5, atom_range)
zv = np.random.uniform(-5, 5, atom_range)
random_velocity = np.random.uniform(-5, 5, 3)

# Initial Velocity and Momentum
a = math.sqrt(random_velocity[0]**2 + random_velocity[1]**2 + random_velocity[2]**2)
initial_velocity = math.sqrt((3 * Kb * T)/(mass_argon))
velocity_vector = initial_velocity * (random_velocity / a)
momentum_vector = mass_argon * velocity_vector

# Apply Initial Velocity to Direction
for i in range(atom_range):
  xv[i] *= momentum_vector[0]
  yv[i] *= momentum_vector[1]
  zv[i] *= momentum_vector[2]

def update(x,y,z,i):
  global xv, yv, zv
  return (x+xv[i], y+yv[i], z+zv[i])

def verletCalculation(force):
  global delta_time, mass_argon
  momantum = momantum + 0.5 * delta_time * force
  r = r + delta_time * momantum / mass_argon
  force = forceCalculation(r)
  momantum = + 0.5 * delta_time * force
  return (momantum, r)

def forceCalculation(r):
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
