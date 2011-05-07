import copy
from math import sqrt

def each_cons(x, size):
    return [x[i:i+size] for i in range(len(x)-size+1)]

class Stroke:
  
  points = []
  
  def __init__(self, points=[]):
    self.points = points
  
  def __eq__(self, other):
    """To reduce duplication, equality is based on hash"""
    return hash(self) == hash(other)
  
  def __hash__(self):
    """If two stroke's points are equal, the strokes are equal"""
    return hash(tuple(self.points))
  
  def __add__(a, b):
    """Adding two strokes concatenates their paths"""
    return Stroke(a.points + b.points)
  
  def centroid(self):
    if(len(self.points) < 1):
      raise ValueError("Centroid cannot be computed without points")
    
    x = sum(point[0] for point in self.points) / len(self.points)
    y = sum(point[1] for point in self.points) / len(self.points)
    
    return (x, y)
  
  def dimensions(self):
    min_point, max_point = self.bounds()
    width = max_point[0] - min_point[0]
    height = max_point[1] - min_point[1]
    return (width, height)
  
  def bounds(self):
    min_x = float("inf")
    min_y = float("inf")
    max_x = float("-inf")
    max_y = float("-inf")
    
    if(len(self.points) < 1):
      return ((0,0), (0,0))
    
    for point in self.points:
      min_x = min(min_x, point[0])
      min_y = min(min_y, point[1])
      max_x = max(max_x, point[0])
      max_y = max(max_y, point[1])
    
    return ((min_x, min_y), (max_x, max_y))
    
  def aspect_ratio(self):
    width, height = self.dimensions()
    return height / width if width > 0 else float('NaN')
  
  def duration(self):
    if(len(self.points) > 0):
      return max(point[2] for point in self.points) # maximum time point
    else:
      return 0
  
  def arc_length(self):
    """Returns the arc length of the stroke"""
    length = 0
    for p1, p2 in each_cons(self.points, 2):
      dx = p1[0] - p2[0]
      dy = p1[1] - p2[1]
      dh = sqrt(dx*dx + dy*dy)
      length += dh
    return length
  
  def smoothed(self):
    """Returns a copy of the stroke with its points smoothed"""
    
    smoothed_stroke = copy.copy(self)
    
    if(len(self.points) < 7):
      return smoothed_stroke
    
    for _ in range(10):
      smoothed_points = []
       
      for p1, p2, p3 in each_cons(smoothed_stroke.points, 3):    
        x = (p1[0] + p2[0] + p3[0]) / 3.0
        y = (p1[1] + p2[1] + p3[1]) / 3.0
      
        smoothed_point = [x, y] + list( p2[2:] )
        smoothed_points.append(tuple(smoothed_point))
        
      smoothed_stroke.points = smoothed_points
    
    return smoothed_stroke