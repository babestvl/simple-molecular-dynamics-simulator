import numpy as np

# initial values
i = 0

test_file = open("fluid.xyz","w")

def cart2sph(x, y, z):
    hxy = np.hypot(x, y)
    r = np.hypot(hxy, z)
    el = np.arctan2(z, hxy)
    az = np.arctan2(y, x)
    return az, el, r

for i in range(10):
  i += 1
  px = np.random.uniform(-1, 1, size=(1, 10000))
  py = np.random.uniform(-1, 1, size=(1, 10000))
  pz = np.random.uniform(-1, 1, size=(1, 10000))
  vx = np.random.random_integers(-1, 1, size=(1, 10000))
  vy = np.random.random_integers(-1, 1, size=(1, 10000))
  vz = np.random.random_integers(-1, 1, size=(1, 10000))
  
  test_file.write("{}\n{}\n".format(len(px[0]),i))
  for i in range(10000):
    px[0][i],py[0][i],pz[0][i] = cart2sph(px[0][i],py[0][i],pz[0][i])
    test_file.write("{} {} {} {}\n".format("H",px[0][i],py[0][i],pz[0][i]))

test_file.close()
