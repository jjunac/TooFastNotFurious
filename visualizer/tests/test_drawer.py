import unittest

from shared import Orientation
from simulator import Road, RightPriorityJunction
from simulator.simulator import Simulator
from visualizer.drawer import Drawer
from visualizer.point import Point


class MyTestCase(unittest.TestCase):

    def test_create_graphic_road(self):
        simulator = Simulator()
        road = Road(simulator, 5, Orientation.NORTH, 1)
        junction = RightPriorityJunction(simulator, 1, 1)
        road2 = Road(simulator, 4, Orientation.WEST, 1)
        road3 = Road(simulator, 3, Orientation.NORTH, 1)

        junction.add_predecessor(Orientation.NORTH, road)
        junction.add_predecessor(Orientation.SOUTH, road3)
        road2.add_predecessor(Orientation.EAST, junction)

        drawing = Drawer(simulator, cell_height=30, cell_length=30)
        roads = drawing.create_graphic_roads(road, Point(200, 500))
        graphic_road = roads[0]
        # self.assertAlmostEqual(0, graphic_road.x)
        # self.assertAlmostEqual(0, graphic_road.y)
        drawing.init_screen()
        drawing.draw()


if __name__ == '__main__':
    unittest.main()
