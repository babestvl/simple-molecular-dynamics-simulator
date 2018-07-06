import numpy as np

class Atom:
  def __init__(self):
    self.id = 0
    self.position_vector = np.random.uniform(-30, 30, 3)
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
delta_time = 0.003
mass_argon = 39.948
mol = 6.022 * (10 ** 23)
T = 300
sphere_radius = 30
border_const = 5
critical_distance = 15
Kb = 8.3 * (10 ** -3)
C6 = 0.0062647225
C12 = 9.847044e-6

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
        force = (((12 * C12) / np.power(distance, 14)) - ((6 * C6) / np.power(distance, 8))) * pos_diff
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

# Testing part
def borderEnergy():
  energy = 0
  for atom in atoms:
    if atom.getDistance() > sphere_radius:
      energy += 0.5 * border_const * np.power((atom.getDistance() - sphere_radius), 2)
  return energy

def vdwEnergy():
  energy = 0
  for atom in atoms:
    for other in atoms:
      if id(atom) != id(other):
        pos_diff = atom.position_vector - other.position_vector
        distance_square = np.sum(np.power(pos_diff, 2))
        distance = np.sqrt(distance_square)
        energy += (C12/np.power(distance, 12)) - (C6/np.power(distance, 6))
  return energy

def kineticEnergy():
  energy = 0
  for atom in atoms:
    energy += 0.5 * mass_argon * np.power(np.mean(atom.momentum_vector)/mass_argon, 2)
  return energy

def totalEnergy():
  border = borderEnergy()
  vdw = vdwEnergy()
  kinetic = kineticEnergy()
  return (border + vdw + kinetic)

# -------------------------

for i in range(2000):
  for atom in atoms:
    verletCalculation(atom)
    if atom.getDistance() > sphere_radius:
      elasticBorder(atom)
  print("{:5} {}".format(i+1, totalEnergy()))

# -------------------------
