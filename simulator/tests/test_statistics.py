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

        car1 = Car(p, entry1, 0)
        car2 = Car(p, entry1, 0)
        car3 = Car(p2, entry2, 0)
        car4 = Car(p, entry3, 0)

        road_cell = []

        for i in range(0, 10):
            road_cell.append(road1.nodes[0][i])

        car1.visited_nodes = road_cell

        stat.add_car_travel(car1)

        road_cell = []

        for i in range(10, 30):
            road_cell.append(road1.nodes[0][i])

        car2.visited_nodes = road_cell

        stat.add_car_travel(car2)

        road_cell = []

        for i in range(50, 70):
            road_cell.append(road1.nodes[0][i])

        car3.visited_nodes = road_cell

        stat.add_car_travel(car3)

        road_cell = []

        for i in range(70, 100):
            road_cell.append(road1.nodes[0][i])

        car4.visited_nodes = road_cell

        stat.add_car_travel(car4)

        self.assertEqual(10, len(stat.list_cars_arrived[(entry1, p)][0].visited_nodes))
        self.assertEqual(20, len(stat.list_cars_arrived[(entry1, p)][1].visited_nodes))
        self.assertEqual(2, len(stat.list_cars_arrived[(entry1, p)]))

        self.assertEqual(20, len(stat.list_cars_arrived[(entry2, p2)][0].visited_nodes))
        self.assertEqual(30, len(stat.list_cars_arrived[(entry3, p)][0].visited_nodes))
        self.assertEqual(2, len(stat.list_cars_arrived[(entry1, p)]))
        self.assertEqual(1, len(stat.list_cars_arrived[(entry2, p2)]))
        self.assertEqual(1, len(stat.list_cars_arrived[(entry3, p)]))

        for i in range(0, 10):
            self.assertEqual(road1.nodes[0][i], stat.list_cars_arrived[(entry1, p)][0].visited_nodes[i])

        for i in range(10, 30):
            self.assertEqual(road1.nodes[0][i], stat.list_cars_arrived[(entry1, p)][1].visited_nodes[i - 10])

        for i in range(50, 70):
            self.assertEqual(road1.nodes[0][i], stat.list_cars_arrived[(entry2, p2)][0].visited_nodes[i - 50])

        for i in range(70, 100):
            self.assertEqual(road1.nodes[0][i], stat.list_cars_arrived[(entry3, p)][0].visited_nodes[i - 70])
