import numpy as np
import math
import time
import datetime

start_time = time.time()

# initial values
count = 0
delta_time = 1 * math.pow(10, -12)
argon_mass = 39.948
mol = 6.022 * math.pow(10, 23)
sigma = 5.670 * math.pow(10, -8)
temp = 300

result_file = open("fluid.xyz","w")

px = np.random.uniform(-1, 1, size=(1, 10000))
py = np.random.uniform(-1, 1, size=(1, 10000))
pz = np.random.uniform(-1, 1, size=(1, 10000))
vx = np.random.random_integers(-1, 1, size=(1, 10000))
vy = np.random.random_integers(-1, 1, size=(1, 10000))
vz = np.random.random_integers(-1, 1, size=(1, 10000))
px,py,pz = px[0],py[0],pz[0]

for i in range(10000):
  r = (px[i]**2)+(py[i]**2)+(pz[i]**2)
  r = r**(1/3)
  if r > 1:
    px[i] = 0
    py[i] = 0
    pz[i] = 0
    count += 1

result_file.write("{}\n{}\n".format(10000-count,1))

for i in range(10000):
  if px[i] != 0:
    result_file.write("{} {} {} {}\n".format("H",px[i],py[i],pz[i]))
      
result_file.close()

print("--- %s seconds ---" % (time.time() - start_time))

def verletCalculation(force):
  global delta_time, argon_mass
  momantum = momantum + 0.5*delta_time*force
  r = r + delta_time*momantum/argon_mass
  force = forceCalculation(r)
  momantum = + 0.5*delta_time*force
  return (momantum,r)

def forceCalulation(r)