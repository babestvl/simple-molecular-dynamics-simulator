import numpy as np
import time
cimport cython
cimport numpy as np

start_time = time.time()

# Initial Values
cdef float delta_time = 0.003
cdef float mass_argon = 39.948
cdef float mol = 6.022e23
cdef float sigma = 0.34
cdef float epsilon = 0.993 
cdef float Kb = 8.3e-3
cdef int T = 300
cdef int sphere_radius = 30
cdef int spring_const = 10
cdef int critical_distance = 15

@cython.boundscheck(False)
@cython.wraparound(False)
cdef getDistance(np.ndarray[np.double_t, ndim=2] position_vectors):
  cdef np.ndarray[np.double_t, ndim=2] vector_square = np.power(position_vectors, 2)
  cdef np.ndarray[np.double_t, ndim=1] r_square = np.sum(vector_square, axis=1)
  cdef np.ndarray[np.double_t, ndim=1] distance = np.sqrt(r_square)
  return distance

@cython.boundscheck(False)
@cython.wraparound(False)
cdef forceCalculation(np.ndarray[np.double_t, ndim=2] position_vectors, np.ndarray[np.double_t, ndim=2] force_vectors, int amount):
  cdef np.ndarray[np.double_t, ndim=3] tiled = np.tile(np.expand_dims(position_vectors, 2), amount)
  cdef np.ndarray[np.double_t, ndim=2] trans = np.transpose(position_vectors)
  cdef np.ndarray[np.double_t, ndim=3] diff = tiled - trans
  cdef np.ndarray[np.double_t, ndim=2] pos_diff
  cdef np.ndarray[np.double_t, ndim=1] distance, force
  cdef np.float64_t x, y
  cdef int i, j
  for i in range(amount):
    pos_diff = np.reshape(diff[i].flatten('F'), (-1, 3))
    distance = np.sqrt(np.sum(np.power(pos_diff, 2), axis=1))
    for j in range(i+1, amount):
      if distance[j] <= critical_distance:
        x = np.power(sigma, 6) / np.power(distance[j], 8)
        y = np.power(sigma, 6) / np.power(distance[j], 6)
        force = 24 * epsilon * x * (2 * y - 1) * pos_diff[j]
        force_vectors[i] += force
        force_vectors[j] -= force
  elasticBorder(position_vectors, force_vectors, amount)

@cython.boundscheck(False)
@cython.wraparound(False)
cdef elasticBorder(np.ndarray[np.double_t, ndim=2] position_vectors, np.ndarray[np.double_t, ndim=2] force_vectors, int amount):
  global sphere_radius, spring_const
  cdef np.ndarray[np.double_t, ndim=1] distance = getDistance(position_vectors)
  cdef np.ndarray[np.double_t, ndim=1] pos_diff = distance - sphere_radius
  cdef np.ndarray[np.double_t, ndim=2] tmp = np.repeat(((-spring_const) * (pos_diff)) / distance, 3).reshape(amount, 3)
  cdef np.ndarray[np.long_t, ndim=2] indexs = np.argwhere(distance > sphere_radius)
  cdef np.ndarray[np.long_t, ndim=1] index = np.reshape(indexs, len(indexs))
  force_vectors[index] += (tmp[index] * position_vectors[index])

@cython.boundscheck(False)
@cython.wraparound(False)
cdef verletCalculation(np.ndarray[np.double_t, ndim=2] position_vectors, np.ndarray[np.double_t, ndim=2] momentum_vectors, np.ndarray[np.double_t, ndim=2] force_vectors, int amount):
  momentum_vectors += 0.5 * delta_time * force_vectors
  position_vectors += delta_time * momentum_vectors / mass_argon
  force_vectors.fill(0)
  forceCalculation(position_vectors, force_vectors, amount)
  momentum_vectors += 0.5 * delta_time * force_vectors

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef main(frame):
  global start_time

  # Initial Atoms and Force
  cdef np.ndarray[np.double_t, ndim=2] position_vectors = np.random.uniform(low=-30, high=30, size=(200, 3))
  cdef np.ndarray[np.double_t, ndim=1] distance = getDistance(position_vectors)
  position_vectors = np.delete(position_vectors, np.argwhere(distance > sphere_radius), 0)
  cdef int amount = len(position_vectors)
  cdef np.ndarray[np.double_t, ndim=2] force_vectors = np.zeros(shape=(amount, 3))

  # Initial Velocity and Momentum
  cdef np.ndarray[np.double_t, ndim=1] random_velocity = np.random.uniform(-3, 3, 3)
  cdef np.float64_t tmp = np.sqrt(np.power(random_velocity[0], 2) + np.power(random_velocity[1], 2) + np.power(random_velocity[2], 2))
  cdef double initial_velocity = np.sqrt((3 * Kb * T)/(mass_argon))
  cdef np.ndarray[np.double_t, ndim=1] velocity_vector = initial_velocity * (random_velocity / tmp)
  cdef np.ndarray[np.double_t, ndim=1] momentum_vector = mass_argon * velocity_vector

  # Apply Initial Momentum to Direction
  cdef np.ndarray[np.double_t, ndim=2] directions = np.random.uniform(low=-3, high=3, size=(amount, 3))
  cdef np.ndarray[np.double_t, ndim=2] momentum_vectors = np.tile(momentum_vector, [amount, 1]) * directions

  result_file = open("out/Test.xyz","w")
  cdef int i
  for i in range(frame):
    verletCalculation(position_vectors, momentum_vectors, force_vectors, amount)
    if i%5==0:
      result_file.write("{}\n{}\n".format(amount, 1))
      for pos in position_vectors:
        result_file.write("{} {} {} {}\n".format("AR", pos[0], pos[1], pos[2]))
  result_file.write("END\n")
  result_file.close()

  print("--- %s seconds ---" % (time.time() - start_time))
