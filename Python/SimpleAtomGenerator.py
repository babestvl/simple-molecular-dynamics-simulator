import numpy as np
import time

start_time = time.time()

class Atom:
  def __init__(self):
    self.id = 0
    self.position_vector = np.random.uniform(-30, 30, 3) # Angstrom
    self.direction = np.random.random_integers(-3, 3, 3)
    self.momentum_vector = 0
    self.force_vector = 0
    
  def getDistance(self):
    vector_square = np.power(self.position_vector,2)
    r_square = np.sum(vector_square)
    distance = np.sqrt(r_square)
    return distance

  def setInitialMomentumVector(self, momentum_vector):
    self.momentum_vector = self.direction * momentum_vector

sphere_radius = 30

# Initial Atoms
atoms = [Atom() for i in range(2000)]

# Delete unusable atoms
usable_atoms = []
for atom in atoms:
  if atom.getDistance() <= sphere_radius:
    usable_atoms.append(atom)
atoms = usable_atoms

for i in range(0, len(atoms)):
  atoms[i].id = i

result_file = open("AtomsSphere.xyz","w")

# -------------------------

result_file.write("{}\n{}\n".format(len(atoms), 1))
for atom in atoms:
  result_file.write("{} {} {} {}\n".format("AR", atom.position_vector[0], atom.position_vector[1], atom.position_vector[2]))

# -------------------------

result_file.write("END\n")
result_file.close()

print("--- %s seconds ---" % (time.time() - start_time))
