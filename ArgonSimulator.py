import numpy as np
import time
import datetime
from Atom import Atom

start_time = time.time()

# Initial Values
delta_time = 0.001 # ps
mass_argon = 39.948
mol = 6.022 * (10**23)
sigma = 3.4 * (10**-10)
epsilon = 1.65 * 0.01
T = 300
R = 5
border_const = 15
# wrong value
# Kb = 2.293 * np.power(10, -50)
# Kb = 1.380 * np.power(10, -23)
Kb = 2.293 * (10**-10)

# Initial Atoms
atoms = [Atom() for i in range(1000)]

# Delete unusable atoms
usable_atoms = []
for atom in atoms:
  if atom.getR() < R:
    usable_atoms.append(atom)
atoms = usable_atoms

# Initial Velocity and Momentum
random_velocity = np.random.uniform(-5, 5, 3)
a = np.sqrt(np.power(random_velocity[0],2) + np.power(random_velocity[1],2) + np.power(random_velocity[2],2))
initial_velocity = np.sqrt((3 * Kb * T)/(mass_argon))
velocity_vector = initial_velocity * (random_velocity / a)
momentum_vector = mass_argon * velocity_vector

# Apply Initial Velocity and Momentum to Direction
for atom in atoms:
  atom.setInitialMomentumVector(momentum_vector)
  atom.setInitialVelocityVector(velocity_vector)

def forceCalculation(r):
  pass

def elasticBorder(atom):
  atom_r = atom.getR()
  border_force = 0
  if atom_r > R:
    border_force = (((-border_const) * (atom_r - R)) / atom_r) * atom.position_vector
  return border_force

def verletCalculation(atom):
  total_force = elasticBorder(atom)
  atom.momentum_vector = atom.momentum_vector + (0.5 * delta_time * total_force)
  atom.position_vector = atom.position_vector + delta_time * atom.momentum_vector / mass_argon
  total_force = forceCalculation(atom.position_vector)
  atom.momentum_vector = atom.momentum_vector + (0.5 * delta_time * total_force)

result_file = open("sample_argon.xyz","w")

# -------------------------

for i in range(1000):
  result_file.write("{}\n{}\n".format(len(atoms),1))
  for atom in atoms:
    result_file.write("{} {} {} {}\n".format("H", atom.position_vector[0], atom.position_vector[1], atom.position_vector[2]))
    verletCalculation(atom)

# -------------------------

result_file.close()

print("--- %s seconds ---" % (time.time() - start_time))
