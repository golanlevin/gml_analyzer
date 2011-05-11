import unittest

from numpy import all, equal
from math import acos, pi

from gml_analyzer.point import Point, PointXYT

class PointTests(unittest.TestCase):
  
  def assertEqualRounded(self, a, b, **kwargs):
    ACCURACY = 6
    self.assertEqual( round(a, ACCURACY), round(b, ACCURACY), **kwargs)
  
  def test_up_right(self):
    joint = (Point((0,0)), Point((0,1)), Point((1,1)))
    self.assertEqualRounded( Point.joint_angle(*joint), pi/2 )
  
  def test_up_left(self):
    joint = (Point((0,0)), Point((0,1)), Point((-1,1)))
    self.assertEqualRounded( Point.joint_angle(*joint), -pi/2 )
  
  def test_left_up(self):
    joint = (Point((0,0)), Point((-1,0)), Point((-1,1)))
    self.assertEqualRounded( Point.joint_angle(*joint), pi/2 )
  
  def test_left_down(self):
    joint = (Point((0,0)), Point((-1,0)), Point((-1,-1)))
    self.assertEqualRounded( Point.joint_angle(*joint), -pi/2 )
  
  def test_down_left(self):
    joint = (Point((0,0)), Point((0,-1)), Point((-1,-1)))
    self.assertEqualRounded( Point.joint_angle(*joint), pi/2 )
  
  def test_down_right(self):
    joint = (Point((0,0)), Point((0,-1)), Point((1,-1)))
    self.assertEqualRounded( Point.joint_angle(*joint), -pi/2 )
  
  def test_right_up(self):
    joint = (Point((0,0)), Point((1,0)), Point((1,1)))
    self.assertEqualRounded( Point.joint_angle(*joint), -pi/2 )
  
  def test_right_down(self):
    joint = (Point((0,0)), Point((1,0)), Point((1,-1)))
    self.assertEqualRounded( Point.joint_angle(*joint), pi/2 )
  
  def test_colinear_joint_angle(self):
    joint = (Point((1,1)), Point((2,1)), Point((3,1)))
    self.assertEqualRounded( Point.joint_angle(*joint), 0 )
  
  def test_last_two_points_same_joint_angle(self):
    joint = (Point((1,1)), Point((2,1)), Point((2,1)))
    self.assertEqualRounded( Point.joint_angle(*joint), 0 )
  
  def test_first_two_points_same_joint_angle(self):
    joint = (Point((1,1)), Point((1,1)), Point((2,1)))
    self.assertEqualRounded( Point.joint_angle(*joint), 0 )
  
  def test_all_points_same_joint_angle(self):
    joint = (Point((0,0)), Point((0,0)), Point((0,0)))
    self.assertEqualRounded( Point.joint_angle(*joint), 0 )
  
  def test_points_folded_on_self_vertically_joint_angle(self):
    joint = (Point((0,0)), Point((1,0)), Point((0,0)))
    self.assertEqualRounded( Point.joint_angle(*joint), pi )
  
  def test_points_folded_on_self_horizontally_joint_angle(self):
    joint = (Point((0,0)), Point((0,1)), Point((0,0)))
    self.assertEqualRounded( Point.joint_angle(*joint), pi )
  
  
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