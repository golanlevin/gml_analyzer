from math import sqrt
from collections import namedtuple

class Point( namedtuple('Point', 'x y') ):
  __slots__ = ()
  
  def __add__(a, b):
    return Point( (a.x + b.x), (a.y + b.y) )
  
  def __sub__(a, b):
    return Point( (a.x - b.x), (a.y - b.y) )
  
  def __div__(a, b):
    return Point( (a.x / b), (a.y / b) )
  
  def distance(a, b):
    delta = a - b
    return sqrt(delta.x ** 2 + delta.y ** 2)

Point.Zero = Point(0, 0)

class PointXYT( namedtuple('PointXYT', 'x y t') ):
  __slots__ = ()
  
  @property
  def xy(self):
    return Point( self.x, self.y )