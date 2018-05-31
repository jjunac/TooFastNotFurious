import unittest
from math import pi

from shared.orientation import Orientation
from simulator import *
from visualizer.drawer import Drawing
from visualizer.road import rotate_point


class MyTestCase(unittest.TestCase):

    def test_search(self):
        road = build_road(5, Orientation.EAST)
        road2 = build_road(5, Orientation.NORTH)
        road3 = build_road(5, Orientation.NORTH)
        entry = EntryNode(1, 0.5)
        entry2 = EntryNode(1, 0.5)
        right_priority = RightPriorityNode()
        link(road[-1], right_priority)
        link(road3[-1], right_priority)
        link(right_priority, road2[0])
        link(entry2, road3[0])
        exit2 = ExitNode()
        link(road2[-1], exit2)
        nodes = road3 + road2 + road
        link(entry, road[0])
        visited, road_map = Drawing.depth_first_search([entry, entry2])
        self.assertEqual(set(nodes), visited)
        roads = [r["road"] for r in road_map]
        self.assertTrue(road in roads)
        self.assertTrue(road2 in roads)
        self.assertTrue(road3 in roads)

        # drawing = Drawing(nodes)
        # drawing.draw()

    def test_rotate_point(self):
        self.assertEqual((10, 0), rotate_point(0, (10, 0)))
        point = (0, -10)
        res = rotate_point(-pi / 2, (10, 0))
        self.assertAlmostEqualTuple(point, res)

        point = (0, 10)
        res = rotate_point(pi / 2, (10, 0))
        self.assertAlmostEqualTuple(point, res)

        point = (-10, 0)
        res = rotate_point(pi, (10, 0))
        self.assertAlmostEqualTuple(point, res)

        point = (0, -10)
        res = rotate_point(3 * pi / 2, (10, 0))
        self.assertAlmostEqualTuple(point, res)

        point = (7.0710678, 7.0710678)
        res = rotate_point(pi / 4, (10, 0))
        self.assertAlmostEqualTuple(point, res)

        point = (5, 5)
        res = rotate_point(pi / 2, (10, 0), (5, 0))
        self.assertAlmostEqualTuple(point, res)

        point = (5, -5)
        res = rotate_point(-pi / 2, (10, 0), (5, 0))
        self.assertAlmostEqualTuple(point, res)

        point = (5, -5)
        res = rotate_point(3 * pi / 2, (10, 0), (5, 0))
        self.assertAlmostEqualTuple(point, res)

        point = (3, 8)
        res = rotate_point(pi / 2, (10, 5), (5, 3))
        self.assertAlmostEqualTuple(point, res)

        point = (5, -5)
        res = rotate_point(pi / 2, (15, 5), (15, -5))
        self.assertAlmostEqualTuple(point, res)

    def assertAlmostEqualTuple(self, point, res):
        self.assertAlmostEqual(point[0], res[0])
        self.assertAlmostEqual(point[1], res[1])


if __name__ == '__main__':
    unittest.main()
