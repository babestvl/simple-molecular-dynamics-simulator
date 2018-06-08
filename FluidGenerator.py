import numpy as np
import math
import time

start_time = time.time()

# initial values
count = 0

test_file = open("fluid.xyz","w")
px = np.random.uniform(-1, 1, size=(1, 10000))
py = np.random.uniform(-1, 1, size=(1, 10000))
pz = np.random.uniform(-1, 1, size=(1, 10000))
vx = np.random.random_integers(-1, 1, size=(1, 10000))
vy = np.random.random_integers(-1, 1, size=(1, 10000))
vz = np.random.random_integers(-1, 1, size=(1, 10000))
px,py,pz = px[0],py[0],pz[0]
for i in range(10000):
  r = (px[i]**2)+(py[i]**2)+(pz[i]**2)
  if r**(1/3) > 1:
    px[i] = 0
    py[i] = 0
    pz[i] = 0
    count += 1
test_file.write("{}\n{}\n".format(10000-count,1))
for i in range(10000):
  if px[i] != 0:
    test_file.write("{} {} {} {}\n".format("H",px[i],py[i],pz[i]))
      
test_file.close()

print("--- %s seconds ---" % (time.time() - start_time))
