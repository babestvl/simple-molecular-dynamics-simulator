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

# Initial Values
delta_time = 0.002
mass_argon = 39.948
mol = 6.022 * (10 ** 23)
sigma = 0.34
epsilon = 0.993 
T = 300
sphere_radius = 30
border_const = 5
critical_distance = 15
Kb = 8.3 * (10 ** -3)

# Initial Atoms
atoms = [Atom() for i in range(200)]

# Delete unusable atoms
usable_atoms = []
for atom in atoms:
  if atom.getDistance() <= sphere_radius:
    usable_atoms.append(atom)
atoms = usable_atoms

for i in range(0, len(atoms)):
  atoms[i].id = i

# Initial Velocity and Momentum
random_velocity = np.random.uniform(-3, 3, 3)
tmp = np.sqrt(np.power(random_velocity[0], 2) + np.power(random_velocity[1], 2) + np.power(random_velocity[2], 2))
initial_velocity = np.sqrt((3 * Kb * T)/(mass_argon))
velocity_vector = initial_velocity * (random_velocity / tmp)
momentum_vector = mass_argon * velocity_vector

# Apply Initial Momentum to Direction
for atom in atoms:
  atom.setInitialMomentumVector(momentum_vector)

def forceCalculation(atom):
  for other in atoms:
    if atom.id < other.id:
      pos_diff = atom.position_vector - other.position_vector
      distance_square = np.sum(np.power(pos_diff, 2))
      distance = np.sqrt(distance_square)
      if distance <= critical_distance:
        x = np.power(sigma, 6) / np.power(distance, 8)
        y = np.power(sigma, 6) / np.power(distance, 6)
        force = 24 * epsilon * x * (2 * y - 1) * pos_diff
        atom.force_vector += force
        other.force_vector -= force

def elasticBorder(atom):
  atom_distance = atom.getDistance()
  border_force = (((-border_const) * (atom_distance - sphere_radius)) / atom_distance) * atom.position_vector
  border_force *= delta_time
  atom.momentum_vector += border_force

def verletCalculation(atom):
  atom.momentum_vector += 0.5 * delta_time * atom.force_vector
  atom.position_vector += delta_time * atom.momentum_vector / mass_argon
  atom.force_vector = 0
  forceCalculation(atom)
  atom.momentum_vector += 0.5 * delta_time * atom.force_vector

result_file = open("sample_argon.xyz","w")

# -------------------------

for i in range(50000):
  for atom in atoms:
    verletCalculation(atom)
    if atom.getDistance() > sphere_radius:
      elasticBorder(atom)
  if i%5==0:
    result_file.write("{}\n{}\n".format(len(atoms), 1))
    for atom in atoms:
      result_file.write("{} {} {} {}\n".format("AR", atom.position_vector[0], atom.position_vector[1], atom.position_vector[2]))

# -------------------------

result_file.write("END\n")
result_file.close()

print("--- %s seconds ---" % (time.time() - start_time))
