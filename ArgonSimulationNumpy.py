import numpy as np
import time

start_time = time.time()

# Initial Values
delta_time = 0.002
mass_argon = 39.948
mol = 6.022e23
sigma = 0.34
epsilon = 0.993 
T = 300
sphere_radius = 30
spring_const = 10
critical_distance = 15
Kb = 8.3e-3

def getDistance():
  global position_vectors
  vector_square = np.power(position_vectors, 2)
  r_square = np.sum(vector_square, axis=1)
  distance = np.sqrt(r_square)
  return distance

def forceCalculation():
  global position_vectors, amount
  for i in range(amount):
    for j in range(amount):
      if i < j:
        pos_diff = position_vectors[i] - position_vectors[j]
        distance_square = np.sum(np.power(pos_diff, 2))
        distance = np.sqrt(distance_square)
        if distance <= critical_distance:
          x = np.power(sigma, 6) / np.power(distance, 8)
          y = np.power(sigma, 6) / np.power(distance, 6)
          force = 24 * epsilon * x * (2 * y - 1) * pos_diff
          force_vectors[i] += force
          force_vectors[j] -= force
  elasticBorder()

def elasticBorder():
  global sphere_radius, spring_const, position_vectors
  distance = getDistance()
  pos_diff = distance - sphere_radius
  tmp = np.repeat(((-spring_const) * (pos_diff)) / distance, 3).reshape(amount, 3)
  index = np.argwhere(distance > sphere_radius)
  index = np.reshape(index, len(index))
  force_vectors[index] += (tmp[index] * position_vectors[index])

def verletCalculation():
  global momentum_vectors, position_vectors, force_vectors
  momentum_vectors += 0.5 * delta_time * force_vectors
  position_vectors += delta_time * momentum_vectors / mass_argon
  force_vectors.fill(0)
  forceCalculation()
  momentum_vectors += 0.5 * delta_time * force_vectors

# Initial Atoms and Force
position_vectors = np.random.uniform(low=-30, high=30, size=(200, 3))
distance = getDistance()
position_vectors = np.delete(position_vectors, np.argwhere(distance > sphere_radius), 0)
amount = len(position_vectors)
force_vectors = np.zeros(shape=(amount, 3))

# Initial Velocity and Momentum
random_velocity = np.random.uniform(-3, 3, 3)
tmp = np.sqrt(np.power(random_velocity[0], 2) + np.power(random_velocity[1], 2) + np.power(random_velocity[2], 2))
initial_velocity = np.sqrt((3 * Kb * T)/(mass_argon))
velocity_vector = initial_velocity * (random_velocity / tmp)
momentum_vector = mass_argon * velocity_vector

# Apply Initial Momentum to Direction
directions = np.random.uniform(low=-3, high=3, size=(amount, 3))
momentum_vectors = np.tile(momentum_vector, [amount, 1]) * directions

result_file = open("Test.xyz","w")

# -------------------------

for i in range(20000):
  verletCalculation()
  if i%5==0:
    result_file.write("{}\n{}\n".format(amount, 1))
    for pos in position_vectors:
      result_file.write("{} {} {} {}\n".format("AR", pos[0], pos[1], pos[2]))

# -------------------------

result_file.write("END\n")
result_file.close()

print("--- %s seconds ---" % (time.time() - start_time))
