import numpy as np

px = np.random.uniform(-0.5, 0.5, size=(1, 10000))
py = np.random.uniform(-0.5, 0.5, size=(1, 10000))
pz = np.random.uniform(-0.5, 0.5, size=(1, 10000))
vx = np.random.random_integers(-1, 1, size=(1, 10000))
vy = np.random.random_integers(-1, 1, size=(1, 10000))
vz = np.random.random_integers(-1, 1, size=(1, 10000))
test_file = open("fluid.xyz","w")
test_file.write("{}\n\n".format(len(px[0])))

for i in range(10000):
  test_file.write("{} {} {} {}\n".format("H",px[0][i],py[0][i],pz[0][i]))
test_file.close()
