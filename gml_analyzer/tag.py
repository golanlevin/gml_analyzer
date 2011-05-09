from lxml import etree
import copy

from stroke import Stroke
from point import Point, PointXYT

class Tag:

  strokes = ()

  def __init__(self, *strokes):
    self.strokes = strokes

  def __eq__(self, other):
    """To reduce duplication, equality is based on hash"""
    return hash(self) == hash(other)

  def __hash__(self):
    """If two tag's strokes are equal, the tags are equal"""
    return hash( tuple(self.strokes) )

  @property
  def duration(self):
    return sum(stroke.duration for stroke in self.strokes)
  
  @property
  def mean_distance_from_centroid(self):
    return self.flattened_stroke().mean_distance_from_centroid
  
  @property
  def std_distance_from_centroid(self):
    return self.flattened_stroke().std_distance_from_centroid


  @property
  def centroid(self):
    return self.flattened_stroke().centroid

  @property
  def stroke_count(self):
    return len(self.strokes)
  
  def flattened_stroke(self):
    return self.flattened().strokes[0]

  def flattened(self):
    """Returns a copy of the tag with all strokes flattened into one stroke"""

    flattened = copy.copy(self)
    
    one_big_stroke = sum( (stroke for stroke in self.strokes), Stroke() )
    flattened.strokes = [ one_big_stroke ]

    return flattened
  
  @property
  def bounds(self):
    return self.flattened_stroke().bounds
  
  @property
  def dimensions(self):
    return self.flattened_stroke().dimensions

  def normalized(self):
    """Returns a copy of the tag with strokes normalized in the range 0..1"""

    normalized = copy.deepcopy(self)
    
    min_point, max_point = self.bounds
    
    width, height = self.dimensions
    normalizing_range = max(width, height)

    for stroke in normalized.strokes:
      stroke.points = [ (point - min_point) / normalizing_range for point in stroke.points ]

    return normalized

  @staticmethod
  def fromGML(gml):
    """Given a GML string, returns a tag object containing the GML's strokes."""

    tag = Tag()
    tag.gml = gml

    root = etree.XML(gml)
    strokes = []

    for stroke in root.findall(".//stroke"):
      points = []

      for point in stroke.findall("pt"):
        x = float( point.find('x').text )
        y = float( point.find('y').text )
        t = point.find('t')
        t = float( t.text ) if t is not None else 0
        points.append( (x,y,t) )

      strokes.append( Stroke(*points) )

    tag.strokes = strokes

    return tag
