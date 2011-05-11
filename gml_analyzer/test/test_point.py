import unittest
from gml_analyzer.point import Point, PointXYT
from numpy import all, equal

class PointTests(unittest.TestCase):
  
  def test_x_getter(self):
    point = Point((1,2))
    self.assertEqual( point.x , 1 )

  def test_y_getter(self):
    point = Point((1,2))
    self.assertEqual( point.y , 2 )
  
  def test_add(self):
    p1 = Point((1,2))
    p2 = Point((3,4))
    self.assertEqual( p1+p2, Point((4,6)) )
  
  def test_subtract(self):
    p1 = Point((1,2))
    p2 = Point((3,4))
    self.assertEqual( p1-p2, Point((-2,-2)) )

  def test_divide_by_scalar(self):
    point = Point((2,4))
    c = 2
    self.assertEqual( point / c, Point((1,2)) )

class PointXYTTests(unittest.TestCase):
  
  def test_x_getter(self):
    point = PointXYT((1,2,3))
    self.assertEqual( point.x , 1 )
  
  def test_y_getter(self):
    point = PointXYT((1,2,3))
    self.assertEqual( point.y , 2 )

  def test_t_getter(self):
    point = PointXYT((1,2,3))
    self.assertEqual( point.t , 3 )
  
  def test_add(self):
    p1 = PointXYT((1,2,3))
    p2 = PointXYT((4,5,6))
    self.assertEqual( p1+p2, PointXYT((5,7,9)) )
  
  def test_subtract(self):
    p1 = PointXYT((1,2,3))
    p2 = PointXYT((4,5,6))
    self.assertEqual( p1-p2, PointXYT((-3, -3, -3)) )
  
  def test_divide_by_scalar(self):
    point = PointXYT((2,4,6))
    c = 2
    self.assertEqual( point / c, PointXYT((1,2,3)) )