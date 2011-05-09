import copy
from numpy import std, mean

from point import Point, PointXYT

def each_cons(x, size):
    return [ x[i:i+size] for i in range( len(x)-size+1 ) ]
def each_pair(x):
    return each_cons(x, 2)

class Stroke:
  
  points = []
  
  def __init__(self, *points):
    """Initialize a new stroke. All arguments are converted into PointXYT objects on init"""
    self.points = map( PointXYT._make, points )
  
  def __eq__(self, other):
    """To reduce duplication, equality is based on hash"""
    return hash(self) == hash(other)
  
  def __hash__(self):
    """If two stroke's points are equal, the strokes are equal"""
    return hash( tuple(self.points) )
  
  def __add__(a, b):
    """Adding two strokes concatenates their paths"""
    return Stroke( *(a.points + b.points) )
  
  def __repr__(self):
    return "<%s %r>" % (self.__class__, self.points)
  
  @property
  def centroid(self):
    """Returns the strokes's center of mass or throws an error if the stroke is empty"""
    if not self.points: raise ValueError("Centroid cannot be computed without points")
    
    return sum( (point.xy for point in self.points), Point.Zero ) / len(self.points)
  
  @property
  def dimensions(self):
    """Returns a tuple containing the stroke's width and height"""
    min_point, max_point = self.bounds
    width, height = max_point - min_point
    
    return ( width, height )
  
  @property
  def bounds(self):
    """Returns a tuple containing the stroke's minimum and maximum point, or (Zero, Zero) if the stroke is empty"""
    if not self.points: return ( Point.Zero, Point.Zero )
    
    minimum = Point(float("inf"), float("inf"))
    maximum = Point(float("-inf"), float("-inf"))
    
    for point in self.points:
      minimum = Point( min(minimum.x, point.x), min(minimum.y, point.y) )
      maximum = Point( max(maximum.x, point.x), max(maximum.y, point.y) )
    
    return ( minimum, maximum )
  
  @property
  def aspect_ratio(self):
    """Returns the ratio of height to width for the stroke, or NaN if the stroke has no width"""
    width, height = self.dimensions
    return height / width if width > 0 else float('NaN')
  
  @property
  def duration(self):
    """Returns the maximum time value for a point in the stroke"""
    return max(point.t for point in self.points) if self.points else 0
  
  @property
  def arc_length(self):
    """Returns the arc length of the stroke"""
    return sum( p1.xy.distance( p2 ) for p1, p2 in each_pair(self.points) )
  
  # def intersection_count(self, other):
  #   """"""
  #   
  #   def intersect(a, b, c, d):
  #     """
  #     Cleverly determine if two lines intersect using the orientation of their points.
  #     
  #     Algorithm fails with overlapping colinear segments, endpoints inside segments, and shared endpoints.
  #     
  #     http://www.bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
  #     """
  #     def ccw(a, b, c):
  #       return (c.y-a.y)*(b.x-a.x) > (b.y-a.y)*(c.x-a.x)
  #     
  #     return ccw(a,c,d) != ccw(b,c,d) and ccw(a,b,c) != ccw(a,b,d)
  #   
  #     count = 0
  #     for a, b in each_pair(self.points):
  #       for c, d in each_pair(other.points):
  #         if( intersect( a, b, c, d ) ):
  #           count += 1
  # 
  #     return count / 2
  # 
  # @property
  # def self_intersection_count(self):
  #   return self.intersection_count(self)
  
  # @property
  # def velocity(self):
  #   velocity = Point.Zero
  #   deltas = [ p2 - p1 for p1, p2 in each_pair(self.points) ]
  #   mean = sum( deltas, Point.Zero ) / len( deltas )
  
  # def velocity_orientation(self):
  #   return self.derivative.orientation
  
  # def velocity_orientedness(self):
  #   return self.derivative.orientedness
  
  # def mean_velocity(self):
  #   return self.derivative.centroid
  
  # def speed(self):
  #   return ( )
  
  # def derivative(self):
  #   return Stroke( p2 - p1 for p1, p2 in each_pair(self.points) )

  # def __principal_components__(self):
  #   '''
  #   
  #   http://stackoverflow.com/questions/4823223/numpy-eig-and-the-percentage-of-variance-in-pca
  #   '''
  #   data = numpy.array( self.points )
  #   data = (data - data.mean(axis=0)) / data.std(axis=0)
  #   c = corrcoef(data, rowvar=0)
  #   return linalg.eig(c)
  # 
  # @property
  # def orientation(self):
  #   values, vectors = self.__principal_components__()
  #   return vectors[0]
  # 
  # @property
  # def orientedness(self):
  #   values, vectors = self.__principal_components__()
  #   return values[0]
  
  # def moments(self):
  
  def __angles__(self):
    """Returns a tuple containing the angle (in radians) between each pair of points in the stroke"""
    return tuple( a.xy.angle( b ) for a, b in each_pair(self.points) )
  
  def __distances_from_centroid__(self):
    """Returns a tuple containing the distance of each point in the stroke from its centroid"""
    centroid = self.centroid

    return tuple( centroid.distance( point ) for point in self.points )
  
  @property
  def std_distance_from_centroid(self):
    """Returns the standard deviation of the distance of each point from the centroid"""
    return std( self.__distances_from_centroid__() )
  
  @property
  def mean_distance_from_centroid(self):
    """Returns the average distance of each point from the centroid"""
    return mean( self.__distances_from_centroid__() )
  
  @property
  def convex_hull(self):
    """
    Computes convex hull via the monotone chain algorithm.
    
    http://en.wikibooks.org/wiki/Algorithm_Implementation/Geometry/Convex_hull/Monotone_chain
    """
    
    points = sorted( set( self.points ) )
    
    if len(points) <= 1: return Stroke(*points)
    
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    
    lower = []
    for point in points:
      while len(lower) >= 2 and cross(lower[-2], lower[-1], point) <= 0:
          lower.pop()
      lower.append(point)

    upper = []
    for point in reversed(points):
      while len(upper) >= 2 and cross(upper[-2], upper[-1], point) <= 0: 
        upper.pop()
      upper.append(point)
  
    hull = lower[:-1] + upper[:-1]
    return Stroke(*hull)

  @property
  def hull_area(self):
    twice_area = sum( (p1.x * p2.y) - (p1.y * p2.x) for p1, p2 in each_pair(self.convex_hull.points) )
    return abs( twice_area / 2 )
  
  # def compactness(self):
  #   return sqrt( self.arc_length ** 2 / hull_area ) if self.hull_area > 0 else 0
  
  # def hull_point_percentage(self):
  #   def clamp(x, low, high):
  #     return min(high, max(low, x))
  #   
  #   stroke_point_count = len(self.points)
  #   hull_point_count = len(self.convex_hull.points)
  #   
  #   if stroke_point_count > 3 and hull_point_count > 3:
  #     percentage = float(hull_point_count) / stroke_point_count
  #     return clamp(percentage, 0, 1)
  #   else:
  #     return 0
  
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