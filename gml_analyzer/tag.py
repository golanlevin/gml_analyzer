from lxml import etree
import copy

from stroke import Stroke

class Tag:

  strokes = []

  def __eq__(self, other):
    """To reduce duplication, equality is based on hash"""
    return hash(self) == hash(other)

  def __hash__(self):
    """If two tag's strokes are equal, the tags are equal"""
    return hash( tuple(self.strokes) )

  def duration(self):
    return sum(stroke.duration() for stroke in self.strokes)

  # def _distances_from_centroid(self):
  #   centroid = self.centroid
  #   flattened = self.flattened()
  #   points = flattened.strokes[0].points
  #   
  #   distances = []
  #   
  #   for point in points
  #     dx = point[0] - centroid[0]
  #     dy = point[1] - centroid[1]
  #     distances.append( sqrt(dx*dx + dy*dy) )
  #   
  #   return distances
  # 
  # def mean_distance_from_centroid(self):
  #   distances = self._distances_from_centroid()
  #   return sum(distances) / len(distances)
  # 
  # def std_dev_distance_from_centroid(self):


  def centroid(self):
    if(len(self.strokes) < 1):
      raise ValueError("Centroid cannot be computed without points")

    x = sum(stroke.centroid()[0] for stroke in self.strokes) / len(self.strokes)
    y = sum(stroke.centroid()[1] for stroke in self.strokes) / len(self.strokes)

    return (x, y)

  def stroke_count(self):
    return len(self.strokes)

  def flattened(self):
    """Returns a copy of the tag with all strokes flattened into one stroke"""

    flattened = copy.copy(self)

    new_stroke = Stroke()
    for stroke in self.strokes:
      new_stroke += stroke

    flattened.strokes = [new_stroke]

    return flattened

  def normalized(self):
    """Returns a copy of the tag with strokes normalized in the range 0..1"""

    normalized = copy.deepcopy(self)

    # TODO: DRY this up
    min_x = float("inf")
    min_y = float("inf")
    min_t = float("inf")
    max_x = float("-inf")
    max_y = float("-inf")
    max_t = float("-inf")

    for stroke in normalized.strokes:
      for point in stroke.points:
        min_x = min(min_x, point[0])
        min_y = min(min_y, point[1])
        min_t = min(min_t, point[2])
        max_x = max(max_x, point[0])
        max_y = max(max_y, point[1])
        max_t = max(max_t, point[2])

    range_x = max_x - min_x
    range_y = max_y - min_y
    range_t = max_t - min_t
    normalizing_range = max(range_x, range_y)

    for stroke in normalized.strokes:
      stroke.points = [ tuple([ (point[0] - min_x) / normalizing_range, (point[1] - min_y) / normalizing_range, point[2] ]) for point in stroke.points ]

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

      strokes.append( Stroke(points) )

    tag.strokes = strokes

    return tag