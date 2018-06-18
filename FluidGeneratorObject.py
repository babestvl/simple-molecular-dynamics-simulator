import numpy as np
import math
import time
import datetime
from Atom import Atom

start_time = time.time()

# Initial Values
count = 0
delta_time = 1 * math.pow(10, -3) # 0.001 ps
mass_argon = 39.948
mol = 6.022 * math.pow(10, 23)
sigma = 5.67 * math.pow(10, -10)
T = 300
R = 5
border_const = 15
# wrong value
# Kb = 2.293 * math.pow(10, -50)
# Kb = 1.380 * math.pow(10, -23)
Kb = 2.293 * math.pow(10, -10)

# Initial Atoms
atoms = [Atom() for i in range(5000)]

# Delete unusable atoms
usable_atoms = []
for atom in atoms:
  if atom.getR() < R:
    usable_atoms.append(atom)
atoms = usable_atoms

# Initial Velocity and Momentum
random_velocity = np.random.uniform(-5, 5, 3)
a = math.sqrt(random_velocity[0]**2 + random_velocity[1]**2 + random_velocity[2]**2)
initial_velocity = math.sqrt((3 * Kb * T)/(mass_argon))
velocity_vector = initial_velocity * (random_velocity / a)
momentum_vector = mass_argon * velocity_vector

# Apply Initial Velocity and Momentum to Direction
for atom in atoms:
  atom.setMomentumVector(momentum_vector)
  atom.setVelocityVector(velocity_vector)

def verletCalculation(force):
  momantum = momantum + 0.5 * delta_time * force
  r = r + delta_time * momantum / mass_argon
  force = forceCalculation(r)
  momantum = + 0.5 * delta_time * force
  return (momantum, r)

def forceCalculation(r):
  pass

def elasticBorder(atom):
  atom_r = atom.getR()
  border_force = ((((-border_const) * (atom_r - R)) / atom_r) * atom.position_vector)
  border_force *= delta_time
  atom.momentum_vector += border_force
  atom.velocity_vector += border_force/mass_argon

def update(atom):
  if atom.getR() > R:
    elasticBorder(atom)
  atom.updatePositionVector()

result_file = open("fluid2.xyz","w")

# -------------------------

for i in range(1000):
  result_file.write("{}\n{}\n".format(len(atoms),1))
  for atom in atoms:
    result_file.write("{} {} {} {}\n".format("H", atom.position_vector[0], atom.position_vector[1], atom.position_vector[2]))
    update(atom)

# -------------------------

result_file.close()

print("--- %s seconds ---" % (time.time() - start_time))
