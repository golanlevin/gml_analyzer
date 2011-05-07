import copy

from point import Point, PointXYT

def each_cons(x, size):
    return [x[i:i+size] for i in range(len(x)-size+1)]

class Stroke:
  
  points = []
  
  def __init__(self, points=[]):
    self.points = map( PointXYT._make, points )
  
  def __eq__(self, other):
    """To reduce duplication, equality is based on hash"""
    return hash(self) == hash(other)
  
  def __hash__(self):
    """If two stroke's points are equal, the strokes are equal"""
    return hash( tuple(self.points) )
  
  def __add__(a, b):
    """Adding two strokes concatenates their paths"""
    return Stroke( a.points + b.points )
  
  @property
  def centroid(self):
    if( len(self.points) < 1 ):
      raise ValueError("Centroid cannot be computed without points")
    
    return sum( (point.xy for point in self.points), Point.Zero ) / len(self.points)
  
  @property
  def dimensions(self):
    min_point, max_point = self.bounds
    width, height = max_point - min_point
    
    return ( width, height )
  
  @property
  def bounds(self):
    minimum = Point(float("inf"), float("inf"))
    maximum = Point(float("-inf"), float("-inf"))
    
    if( len(self.points) < 1 ):
      return ( Point.Zero, Point.Zero )
    
    for point in self.points:
      minimum = Point( min(minimum.x, point.x), min(minimum.y, point.y) )
      maximum = Point( max(maximum.x, point.x), max(maximum.y, point.y) )
    
    return ( minimum, maximum )
  
  @property
  def aspect_ratio(self):
    width, height = self.dimensions
    return height / width if width > 0 else float('NaN')
  
  @property
  def duration(self):
    if( len(self.points) > 0 ):
      return max(point.t for point in self.points) if(len(self.points) > 0) else 0
    else:
      return 0
  
  @property
  def arc_length(self):
    """Returns the arc length of the stroke"""
    return sum( p1.xy.distance( p2.xy ) for p1, p2 in each_cons(self.points, 2) )
  
  def smoothed(self):
    """Returns a copy of the stroke with its points smoothed"""
    
    smoothed_stroke = copy.copy(self)
    
    if(len(self.points) < 7):
      return smoothed_stroke

    for _ in xrange(10):
      
      # Repeat first and last so the ends smooth too
      smooth_array = [smoothed_stroke.points[0]] + smoothed_stroke.points + [smoothed_stroke.points[-1]]
  
      smoothed_points = []
      for p1, p2, p3 in each_cons(smooth_array, 3):
        smoothed = (p1.xy + p2.xy + p3.xy) / 3.0
        smoothed_points.append( PointXYT(smoothed.x, smoothed.y, p2.t) )
  
      smoothed_stroke.points = smoothed_points
    
    return smoothed_stroke