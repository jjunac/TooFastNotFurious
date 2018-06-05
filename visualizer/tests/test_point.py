import unittest
from math import pi

from visualizer.point import Point, to_radians, to_degrees


def find_road(road, road_map):
    return [r for r in road_map if r["road"] == road][0]


class TestPoint(unittest.TestCase):

    def test_rotate_point(self):
        origin = Point(0, 0)
        print(origin)
        base_point = Point(10, 0)
        self.assertEqual(base_point, origin.rotate_point(0, base_point))
        point = Point(0, -10)
        res = origin.rotate_point(-180 / 2, base_point)
        self.assertAlmostEqualPoint(point, res)

        point = Point(0, 10)
        res = origin.rotate_point(180 / 2, base_point)
        self.assertAlmostEqualPoint(point, res)

        point = Point(-10, 0)
        res = origin.rotate_point(180, base_point)
        self.assertAlmostEqualPoint(point, res)

        point = Point(0, -10)
        res = origin.rotate_point(3 * 180 / 2, base_point)
        self.assertAlmostEqualPoint(point, res)

        point = Point(7.0710678, 7.0710678)
        res = origin.rotate_point(180 / 4, base_point)
        self.assertAlmostEqualPoint(point, res)

        point = Point(5, 5)
        origin = Point(5, 0)
        res = origin.rotate_point(180 / 2, base_point)
        self.assertAlmostEqualPoint(point, res)

        point = Point(5, -5)
        res = origin.rotate_point(-180 / 2, base_point)
        self.assertAlmostEqualPoint(point, res)

        point = Point(5, -5)
        res = origin.rotate_point(3 * 180 / 2, base_point)
        self.assertAlmostEqualPoint(point, res)

        point = Point(3, 8)
        origin = Point(5, 3)
        res = origin.rotate_point(180 / 2, Point(10, 5))
        self.assertAlmostEqualPoint(point, res)

        point = Point(5, -5)
        origin = Point(15, -5)
        res = origin.rotate_point(180 / 2, Point(15, 5))
        self.assertAlmostEqualPoint(point, res)

        point = Point(-1, 5)
        origin = Point(0, 0)
        res = origin.rotate_point(360, Point(-1, 5))
        self.assertAlmostEqualPoint(point, res)

        point = Point(-5, 0)
        origin = Point(0, 0)
        res = origin.rotate_point(450, Point(0, 5))
        self.assertAlmostEqualPoint(point, res)

    def assertAlmostEqualPoint(self, point, res):
        self.assertAlmostEqual(point.x, res.x)
        self.assertAlmostEqual(point.y, res.y)

    def test_conversions(self):
        self.assertAlmostEqual(pi, to_radians(180))
        self.assertAlmostEqual(pi / 2, to_radians(90))
        self.assertAlmostEqual(pi / 4, to_radians(45))
        self.assertAlmostEqual(3 * pi / 2, to_radians(270))

        self.assertAlmostEqual(180, to_degrees(pi))
        self.assertAlmostEqual(180 / 2, to_degrees(pi / 2))
        self.assertAlmostEqual(180 / 4, to_degrees(pi / 4))

        self.assertAlmostEqual(45, to_degrees(to_radians(45)))

        self.assertAlmostEqual(90, to_degrees(to_radians(90)))

        self.assertAlmostEqual(pi, to_radians(to_degrees(pi)))


if __name__ == '__main__':
    unittest.main()
