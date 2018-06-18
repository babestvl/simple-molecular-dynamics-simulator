import numpy as np
import math

class Atom:
  def __init__(self):
    self.position_vector = np.random.uniform(-1, 1, 3)
    self.direction = np.random.random_integers(-1, 1, 3)
    self.velocity_vector = 0
    self.momentum_vector = 0

  def getR(self):
    return math.sqrt(np.sum(self.position_vector**2))

  def setVelocityVector(self, velocity_vector):
    self.velocity_vector = self.direction * velocity_vector

  def setMomentum_vector(self, momentum_vector):
    self.momentum_vector = self.direction * momentum_vector

  def updatePosition_vector(self):
    self.position_vector += self.momentum_vector
    