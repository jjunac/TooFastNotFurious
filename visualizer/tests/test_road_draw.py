import unittest
from math import pi

from shared.orientation import Orientation
from simulator import *
from visualizer.drawer import Drawing
from visualizer.road import rotate_point


def find_road(road, road_map):
    return [r for r in road_map if r["road"] == road][0]


class TestRoadDraw(unittest.TestCase):

    @unittest.skip("Need to refactor the test according to new simulator api")
    def test_search(self):
        # FIXME Need to refactor the test according to new simulator api
        road = build_road(5, Orientation.EAST)
        road2 = build_road(5, Orientation.NORTH)
        road3 = build_road(5, Orientation.NORTH)
        road4 = build_road(5, Orientation.EAST)
        entry = EntryNode(1, 0.3)
        entry.paths[100] = Path([0] * 13)
        entry2 = EntryNode(1, 0.1)
        entry2.paths[100] = Path([0] * 13)

        exit1 = ExitNode()
        exit2 = ExitNode()
        link(entry, road[0])
        link(entry2, road3[0])
        link(road2[-1], exit1)
        link(road4[-1], exit2)
        priority_node = RightPriorityNode()
        link(road[-1], priority_node)
        link(road3[-1], priority_node)
        link(priority_node, road2[0])
        link(priority_node, road4[0])
        nodes = road + road2 + road3 + road4
        visited, road_map = Drawing.depth_first_search([entry, entry2])
        self.assertEqual(set(nodes), visited)
        roads = [r["road"] for r in road_map]
        self.assertTrue(road in roads)
        self.assertTrue(road2 in roads)
        self.assertTrue(road3 in roads)
        self.assertTrue(road4 in roads)
        self.assert_correct_road_entry_and_exit(entry, road, priority_node, road_map)
        self.assert_correct_road_entry_and_exit(entry2, road3, priority_node, road_map)
        self.assert_correct_road_entry_and_exit(priority_node, road2, exit1, road_map)
        self.assert_correct_road_entry_and_exit(priority_node, road4, exit2, road_map)

    def assert_correct_road_entry_and_exit(self, entry, road, exit, road_map):
        road_m = find_road(road, road_map)
        self.assertEqual(entry, road_m["entry"])
        self.assertEqual(exit, road_m["exit"])

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
