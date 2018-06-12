import unittest

from shared import Orientation
from simulator import Road, RightPriorityJunction
from simulator.simulator import Simulator
from visualizer.drawer import Drawer
from visualizer.point import Point


class MyTestCase(unittest.TestCase):

    @unittest.skip
    def test_create_graphic_road(self):
        simulator = Simulator()
        # FIXME
        road = Road(simulator, 5, Orientation.EAST, 1)
        junction = RightPriorityJunction(simulator, {Orientation.NORTH: (1, 0), Orientation.EAST: (1, 1),
                                                     Orientation.SOUTH: (0, 1), Orientation.WEST: (0, 0)})
        road2 = Road(simulator, 6, Orientation.NORTH, 1)
        road3 = Road(simulator, 2, Orientation.WEST, 1)
        road4 = Road(simulator, 4, Orientation.WEST, 1)
        road5 = Road(simulator, 3, Orientation.NORTH, 1)
        road6 = Road(simulator, 5, Orientation.WEST, 1)

        junction.add_predecessor(Orientation.EAST, road)
        junction.add_predecessor(Orientation.NORTH, road2)

        road2.add_predecessor(Orientation.EAST, road4)
        road2.add_predecessor(Orientation.NORTH, road5)
        road3.add_predecessor(Orientation.WEST, junction)
        road5.add_predecessor(Orientation.EAST, road6)

        cell_size = 30
        drawing = Drawer(simulator, cell_height=cell_size, cell_length=cell_size)
        roads = drawing.create_graphic_roads(road, Point(0, 0))
        graphic_road = roads[0]

        self.assertEqual(Point(0, 0), graphic_road.start)
        self.assertEqual(Point(cell_size, 0), graphic_road.sprite_start)
        road0_end = Point(6 * cell_size, 0)
        self.assertEqual(road0_end, graphic_road.end)
        self.assertEqual(Point(5 * cell_size, 0), graphic_road.sprite_end)
        # FIXME
        # self.assertEqual(road0_end, roads[2].start)
        # self.assertEqual(road0_end + Point(cell_size, 0), roads[2].sprite_start)
        # size_ = road0_end + Point(3 * cell_size, 0)
        # self.assertEqual(size_, roads[2].end)
        # self.assertEqual(road0_end + Point(2 * cell_size, 0), roads[2].sprite_end)

        # TODO continue test

if __name__ == '__main__':
    unittest.main()
