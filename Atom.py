import numpy as np

class Atom:
  def __init__(self):
    self.position_vector = np.random.uniform(-10, 10, 3)
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
