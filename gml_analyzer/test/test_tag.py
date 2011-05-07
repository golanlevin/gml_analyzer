import unittest
from lxml.etree import XMLSyntaxError
from nose.tools import raises

from gml_analyzer.tag import Tag
from gml_analyzer.stroke import Stroke

class TagTests(unittest.TestCase):
  
  @raises(ValueError)
  def test_empty_centroid(self):
    tag = Tag()
    tag.centroid
  
  def test_centroid(self):
    tag = Tag()
    tag.strokes = [Stroke([(0,0,0)]), Stroke([(2,2,2)])]
    self.assertEqual(tag.centroid, (1,1))
  
  def test_empty_duration(self):
    tag = Tag()
    self.assertEqual(tag.duration, 0)
    
  def test_duration(self):
    tag = Tag()
    tag.strokes = [Stroke([(0,0,1)]), Stroke([(0,0,2)])]
    self.assertEqual(tag.duration, 3)
  
  def test_stroke_count(self):
    tag = Tag()
    self.assertEqual(tag.stroke_count, 0)
  
  def test_stroke_count(self):
    tag = Tag()
    tag.strokes = [Stroke([(0,0,0)])]
    self.assertEqual(tag.stroke_count, 1)
  
  def test_empty_strokes_array(self):
    tag = Tag()
    self.assertEqual(tag.strokes, [])
  
  def test_empty_tags_equal(self):
    t1 = Tag()
    t2 = Tag()
    self.assertEqual(t1, t2)
    
  def test_empty_tags_have_same_hash(self):
    t1 = Tag()
    t2 = Tag()
    self.assertEqual(hash(t1), hash(t2))
  
  def test_degenerate_gml_string(self):
    self.assertRaises(XMLSyntaxError, Tag.fromGML, "")
  
  def test_normalized(self):
    tag = Tag()
    tag.strokes = [Stroke([(-5,-5,-5), (5,5,5)])]
    normalized = tag.normalized()
    self.assertEqual(normalized.strokes[0].points, [(0,0,-5), (1,1,5)])
  
  def test_normalized_doesnt_change_original(self):
    tag = Tag()
    tag.strokes = [Stroke([(-5,-5,-5), (5,5,5)])]
    normalized = tag.normalized()
    self.assertEqual(normalized.strokes[0].points, [(0,0,-5), (1,1,5)])
    self.assertEqual(tag.strokes[0].points, [(-5,-5,-5), (5,5,5)])
  
  def test_flattened(self):
    tag = Tag()
    tag.strokes = [Stroke([(0,0,0)]), Stroke([(1,1,1)])]
    flattened = tag.flattened()
    self.assertEqual(flattened.strokes[0].points, [(0,0,0), (1,1,1)])
  
  def test_flattened_doesnt_change_original(self):
    tag = Tag()
    tag.strokes = [Stroke([(0,0,0)]), Stroke([(1,1,1)])]
    flattened = tag.flattened()
    self.assertEqual(flattened.strokes[0].points, [(0,0,0), (1,1,1)])
    self.assertEqual(tag.strokes[0].points, [(0,0,0)])
  
  def test_simple_gml_string(self):
    gml = """<gml>
      <drawing>
        <stroke>
          <pt><x>1</x><y>1</y><t>1</t></pt>
        </stroke>
      </drawing>
    </gml>"""
    tag = Tag.fromGML(gml)
    self.assertEqual( tag.strokes[0].points[0], (1,1,1) )