import unittest

from visualizer.point import Point
from visualizer.road import GraphicRoad

cell_size = 30


class MyTestCase(unittest.TestCase):

    def test_creation(self):
        start = Point(0, 0)
        end = Point(300, 0)
        road = GraphicRoad(start, end, [], cell_size, cell_size)
        self.assertRoad(road, start, end, start + Point(cell_size, 0), end - Point(cell_size, 0), 0, Point(30, 0))

        start = Point(0, 0)
        end = Point(0, 300)
        road = GraphicRoad(start, end, [], cell_size, cell_size)
        self.assertRoad(road, start, end, start + Point(0, cell_size), end - Point(0, cell_size), 90, Point(0, 30))

        start = Point(0, 0)
        end = Point(0, -300)
        road = GraphicRoad(start, end, [], cell_size, cell_size)
        self.assertRoad(road, start, end, start - Point(0, cell_size), end + Point(0, cell_size), -90, Point(0, -30))

        start = Point(0, 0)
        end = Point(-300, 0)
        road = GraphicRoad(start, end, [], cell_size, cell_size)
        self.assertRoad(road, start, end, start - Point(cell_size, 0), end + Point(cell_size, 0), 180, Point(-30, 0))

    def assertRoad(self, road, start, end, sprite_start, sprite_end, angle, pos_i):
        self.assertEqual(start, road.start)
        self.assertEqual(end, road.end)
        self.assertEqual(sprite_start, road.sprite_start)
        self.assertEqual(sprite_end, road.sprite_end)
        self.assertEqual(pos_i, road.pos_i)
        self.assertAlmostEqual(angle, road.angle)


if __name__ == '__main__':
    unittest.main()
