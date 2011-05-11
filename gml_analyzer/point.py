from math import sqrt, acos, degrees, copysign, pi
from collections import namedtuple
from numpy import ndarray, arccos, asarray, vdot, abs, linalg
import numpy

class Point(ndarray):
  
  def __new__(klass, input_array, dtype=float):
    if len(input_array) != 2: raise ValueError("Point must have two elements")
    
    return asarray(input_array, dtype=float).view(klass)
  
  def __eq__(self, other):
    return numpy.equal(self, other).all()
  
  @property
  def x(self):
    return self[0]
  
  @property
  def y(self):
    return self[1]
  
  def angle(a, b):
    return arccos( vdot(a, b) / vabs(a) / vabs(b) )
  
  def joint_angle(A, C, B):
    a = C.distance(B)
    b = A.distance(C)
    c = B.distance(A)
    
    if a == 0 or b == 0: return 0
    
    def signed_area(p1, p2, p3):
      return (p2.x - p1.x)*(p3.y - p1.y) - (p2.y - p1.y)*(p3.x - p1.x)
    
    theta = pi - acos( (a**2 + b**2 - c**2) / (2.0 * a * b) )
    
    return copysign(theta, signed_area(A,B,C))
  
  def distance(a, b):
    return linalg.norm(a - b)

Point.Zero = Point((0, 0))

class PointXYT(Point):
  
  def __new__(klass, input_array):
    if len(input_array) != 3: raise ValueError("PointXYT must have 3 elements")
    
    return asarray(input_array).view(klass)

  def __eq__(self, other):
    return numpy.equal(self, other).all()

  @property
  def x(self):
    return self[0]

  @property
  def y(self):
    return self[1]

  @property
  def t(self):
    return self[2]
  
  @property
  def xy(self):
    return Point( (self.x, self.y) )