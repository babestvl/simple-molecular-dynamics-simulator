import numpy as np
import math
import time
import datetime

start_time = time.time()

# initial values
count = 0
delta_time = 1 * math.pow(10, -12)
mass_argon = 39.948
mol = 6.022 * math.pow(10, 23)
sigma = 5.670 * math.pow(10, -8)
T = 300
R = 1
Kb = 2.293 * math.pow(10, -47)

result_file = open("fluid.xyz","w")

#Position
xp = np.random.uniform(-1, 1, 10000)
yp = np.random.uniform(-1, 1, 10000)
zp = np.random.uniform(-1, 1, 10000)

#Velocity
random_velocity = np.random.uniform(-5, 5, 3)

#Initial Velocity
a = math.sqrt(random_velocity[0]**2 + random_velocity[1]**2 + random_velocity[2]**2)
initial_velocity = math.sqrt((3 * Kb * T)/(mass_argon))
velocity_vector = initial_velocity * (random_velocity/a)
momentum_vector = mass_argon * velocity_vector

def update(x,y,z):
  return (x+np.random.uniform(-1,1,1), y+np.random.uniform(-1,1,1), z+np.random.uniform(-1,1,1))

def verletCalculation(force):
  global delta_time, mass_argon
  momantum = momantum + 0.5*delta_time*force
  r = r + delta_time*momantum/mass_argon
  force = forceCalculation(r)
  momantum = + 0.5*delta_time*force
  return (momantum,r)

def forceCalulation(r):
  pass

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

# -------------------------

for j in range(1000):
  result_file.write("{}\n{}\n".format(len(xp),1))
  for i in range(len(xp)):
    if xp[i] != 0:
      result_file.write("{} {} {} {}\n".format("H",xp[i],yp[i],zp[i]))
      xp[i],yp[i],zp[i] = update(xp[i],yp[i],zp[i])
      
# -------------------------


result_file.close()

print("--- %s seconds ---" % (time.time() - start_time))
