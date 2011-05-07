import unittest
import math
from nose.tools import raises

from gml_analyzer.stroke import Stroke

class StrokeTests(unittest.TestCase):
  
  @raises(ValueError)
  def test_empty_centroid(self):
    stroke = Stroke()
    stroke.centroid
  
  def test_zero_centroid(self):
    stroke = Stroke([(0,0,0)])
    self.assertEqual( stroke.centroid, (0,0) )
  
  def test_square_centroid(self):
    stroke = Stroke([(0,0,0), (2,2,2)])
    self.assertEqual( stroke.centroid, (1,1) )
  
  def test_rectangular_centroid(self):
    stroke = Stroke([(0,0,0), (4,2,0)])
    self.assertEqual( stroke.centroid, (2,1) )
  
  def test_zero_duration(self):
    stroke = Stroke()
    self.assertEqual(stroke.duration, 0)
  
  def test_duration(self):
    stroke = Stroke([(0,0,1)])
    self.assertEqual(stroke.duration, 1)
  
  def test_longer_duration(self):
    stroke = Stroke([(0,0,1),(0,0,2)])
    self.assertEqual(stroke.duration, 2)
  
  def test_zero_arc_length(self):
    stroke = Stroke()
    self.assertEqual(stroke.arc_length, 0)
  
  def test_one_arc_length(self):
    stroke = Stroke([(0,0,0),(1,0,0)])
    self.assertEqual(stroke.arc_length, 1)
  
  def test_empty_stroke(self):
    stroke = Stroke()
    self.assertEqual(stroke.points, [])
    
  def test_concatenation(self):
    s1 = Stroke([(0,0,0)])
    s2 = Stroke([(1,1,1)])
    s1 += s2
    self.assertEqual(s1.points, [(0,0,0), (1,1,1)])
  
  def test_one_point_stroke(self):
    stroke = Stroke([(0,0,0)])
    self.assertEqual(stroke.points, [(0,0,0)])
  
  def test_empty_strokes_equal(self):
    s1 = Stroke()
    s2 = Stroke()
    self.assertEqual(s1, s2)
  
  def test_strokes_with_same_points_equal(self):
    s1 = Stroke([(1,1,1)])
    s2 = Stroke([(1,1,1)])
    self.assertEqual(s1, s2)
  
  def test_empty_strokes_have_same_hash(self):
    s1 = Stroke()
    s2 = Stroke()
    self.assertEqual(hash(s1), hash(s2))
  
  def test_smoothed_too_few_points(self):
    stroke = Stroke([(4,4,4),(1,1,1),(4,4,4)])
    smoothed = stroke.smoothed()
    self.assertEqual(smoothed.points, [(4,4,4),(1,1,1),(4,4,4)])
  
  def test_smoothed_equal_points(self):
    points = [ (1,1,1) ] * 7
    stroke = Stroke(points)
    smoothed = stroke.smoothed()
    self.assertEqual(smoothed.points, points)
  
  def test_smoothed_with_blending(self):
    points = [ (1,1,1), (0,0,0) ] * 4
    stroke = Stroke(points)
    smoothed = stroke.smoothed()
    self.assertTrue( smoothed.points[1][0] > 0 )
    self.assertTrue( smoothed.points[2][0] < 1 )
  
  def test_strokes_with_same_points_have_same_hash(self):
    s1 = Stroke([(1,1,1)])
    s2 = Stroke([(1,1,1)])
    self.assertEqual(hash(s1), hash(s2))
  
  def test_bounds(self):
    stroke = Stroke([(-1,-1,-1),(1,1,1)])
    self.assertEqual(stroke.bounds, ((-1,-1),(1,1)))
  
  def test_zero_bounds(self):
    stroke = Stroke()
    self.assertEqual(stroke.bounds, ((0,0), (0,0)))
  
  def test_dimensions(self):
    stroke = Stroke([(-1,-1,-1),(1,1,1)])
    self.assertEqual(stroke.dimensions, (2,2))
  
  def test_zero_dimensions(self):
    stroke = Stroke()
    self.assertEqual(stroke.dimensions, (0,0))
  
  def test_degenerate_aspect_ratio(self):
    stroke = Stroke()
    self.assertTrue( math.isnan(stroke.aspect_ratio) )
  
  def test_aspect_ratio(self):
    stroke = Stroke([(0,0,0),(1,0,0)])
    self.assertEqual( stroke.aspect_ratio, 0 )
  
  def test_aspect_ratio(self):
    stroke = Stroke([(1,1,1),(0,0,0)])
    self.assertEqual( stroke.aspect_ratio, 1 )