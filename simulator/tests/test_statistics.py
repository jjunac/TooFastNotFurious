import unittest

from shared import Orientation
from simulator import *


class TestStatistics(unittest.TestCase):

    def test_sould_add_travel_path(self):
        simulator = Simulator()
        entry1 = Entry(simulator, 0, 1)
        entry2 = Entry(simulator, 0, 1)
        entry3 = Entry(simulator, 0, 1)

        p = Path([])
        p2 = Path([])

        # road to south
        road1 = Road(simulator, 100, Orientation.SOUTH, 1)
        road1.add_predecessor(Orientation.SOUTH, entry1)

        stat = Statistics()

        self.assertFalse(p in stat.list_cars_arrived)
        self.assertFalse(p2 in stat.list_cars_arrived)

        road_cell = []

        for i in range(0, 10):
            road_cell.append(road1.nodes[0][i])

        stat.add_car_travel(entry1, p, road_cell)

        road_cell = []

        for i in range(10, 30):
            road_cell.append(road1.nodes[0][i])

        stat.add_car_travel(entry1, p, road_cell)

        road_cell = []

        for i in range(50, 70):
            road_cell.append(road1.nodes[0][i])

        stat.add_car_travel(entry2, p2, road_cell)

        road_cell = []

        for i in range(70, 100):
            road_cell.append(road1.nodes[0][i])

        stat.add_car_travel(entry3, p, road_cell)

        self.assertEqual(10, len(stat.list_cars_arrived[(entry1, p)][0]))
        self.assertEqual(20, len(stat.list_cars_arrived[(entry1, p)][1]))
        self.assertEqual(2, len(stat.list_cars_arrived[(entry1, p)]))

        self.assertEqual(20, len(stat.list_cars_arrived[(entry2, p2)][0]))
        self.assertEqual(30, len(stat.list_cars_arrived[(entry3, p)][0]))
        self.assertEqual(2, len(stat.list_cars_arrived[(entry1, p)]))
        self.assertEqual(1, len(stat.list_cars_arrived[(entry2, p2)]))
        self.assertEqual(1, len(stat.list_cars_arrived[(entry3, p)]))

        for i in range(0, 10):
            self.assertEqual(road1.nodes[0][i], stat.list_cars_arrived[(entry1, p)][0][i])

        for i in range(10, 30):
            self.assertEqual(road1.nodes[0][i], stat.list_cars_arrived[(entry1, p)][1][i - 10])

        for i in range(50, 70):
                self.assertEqual(road1.nodes[0][i], stat.list_cars_arrived[(entry2, p2)][0][i - 50])

        for i in range(70, 100):
                self.assertEqual(road1.nodes[0][i], stat.list_cars_arrived[(entry3, p)][0][i - 70])
