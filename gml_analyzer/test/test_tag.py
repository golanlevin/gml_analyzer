import unittest
from lxml.etree import XMLSyntaxError
from nose.tools import raises

from gml_analyzer.tag import Tag
from gml_analyzer.stroke import Stroke
from gml_analyzer.point import Point, PointXYT

class TagTests(unittest.TestCase):
  
  def setUp(self):
    self.empty_tag = Tag()
  
  @raises(ValueError)
  def test_empty_centroid(self):
    self.empty_tag.centroid
  
  @raises(ValueError)
  def test_empty_mean_distance_from_centroid(self):
    self.empty_tag.mean_distance_from_centroid
  
  def test_equal_mean_distance_from_centroid(self):
    tag = Tag( Stroke((-1,0,0)), Stroke((1,0,0)))
    self.assertEqual( tag.mean_distance_from_centroid, 1 )
  
  def test_mean_distance_from_centroid(self):
    tag = Tag( Stroke((0,-1,0)), Stroke((0,3,0)))
    self.assertEqual( tag.mean_distance_from_centroid, 2 )
  
  def test_std_distance_from_centroid(self):
    tag = Tag( Stroke((0,0,0)), Stroke((0,1,0)))
    self.assertEqual( tag.std_distance_from_centroid, 0.5 )
  
  def test_centroid(self):
    tag = Tag( Stroke((0,0,0)), Stroke((2,2,2)) )
    self.assertEqual(tag.centroid, (1,1))
  
  def test_empty_duration(self):
    self.assertEqual(self.empty_tag.duration, 0)
    
  def test_duration(self):
    tag = Tag( Stroke((0,0,1)), Stroke((0,0,2)) )
    self.assertEqual(tag.duration, 3)
  
  def test_empty_strokes_array(self):
    self.assertEqual(self.empty_tag.strokes, ())
  
  def test_empty_tags_equal(self):
    t1 = Tag()
    t2 = Tag()
    self.assertEqual(t1, t2)
    
  def test_empty_tags_have_same_hash(self):
    t1 = Tag()
    t2 = Tag()
    self.assertEqual(hash(t1), hash(t2))
  
  @raises(XMLSyntaxError)
  def test_degenerate_gml_string(self):
    Tag.fromGML("")
  
  def test_zero_bounds(self):
    self.assertEqual(self.empty_tag.bounds, (Point.Zero, Point.Zero))
    
  def test_bounds(self):
    tag = Tag( Stroke((0,0,0)), Stroke((1,1,1)) )
    self.assertEqual( tag.bounds, ((0,0), (1,1)) )
  
  def test_zero_dimensions(self):
    self.assertEqual( self.empty_tag.dimensions, (0,0) )
    
  def test_dimesions(self):
    tag = Tag( Stroke((-1,-1,-1)), Stroke((1,1,1)) )
    self.assertEqual( tag.dimensions, (2,2) )
  
  def test_normalized(self):
    tag = Tag( Stroke((-5,-5,-5), (5,5,5)) )
    normalized = tag.normalized()
    self.assertEqual( normalized.strokes[0], Stroke((0,0,-5), (1,1,5)) )
  
  def test_normalized_doesnt_change_original(self):
    tag = Tag( Stroke((-5,-5,-5), (5,5,5)) )
    normalized = tag.normalized()
    self.assertEqual( tag.strokes[0], Stroke((-5,-5,-5), (5,5,5)) )
  
  def test_empty_flattened_stroke(self):
    self.assertEqual( self.empty_tag.flattened_stroke(), Stroke() )
  
  def test_flattened_stroke(self):
    tag = Tag( Stroke((0,0,0)), Stroke((1,1,1)) )
    self.assertEqual( tag.flattened_stroke(), Stroke((0,0,0), (1,1,1)) )

  def test_simple_gml_string(self):
    gml = """<gml>
      <drawing>
        <stroke>
          <pt><x>1</x><y>1</y><t>1</t></pt>
        </stroke>
      </drawing>
    </gml>"""
    tag = Tag.fromGML(gml)
    self.assertEqual( tag.strokes[0], Stroke((1,1,1)) )