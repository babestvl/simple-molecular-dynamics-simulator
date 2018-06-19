import numpy as np

class Atom:
  def __init__(self):
    self.position_vector = np.random.uniform(-15, 15, 3)
    self.direction = np.random.random_integers(-1, 1, 3)
    self.velocity_vector = 0
    self.momentum_vector = 0
    self.force_vector = 0
    
  def getR(self):
    vector_square = np.power(self.position_vector,2)
    r_square = np.sum(vector_square)
    r = np.sqrt(r_square)
    return r

  def setInitialVelocityVector(self, velocity_vector):
    self.velocity_vector = self.direction * velocity_vector

  def setInitialMomentumVector(self, momentum_vector):
    self.momentum_vector = self.direction * momentum_vector
