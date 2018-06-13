import unittest

from shared import *
from simulator import Simulator
from simulator.car import Car
from simulator.road import Road
from simulator.path import Path
from simulator.utils import *


class TestRoad(unittest.TestCase):

    def test_a_car_should_go_forward_when_it_is_alone(self):
        simulator = Simulator()
        road = Road(simulator, 10, Orientation.NORTH, 1)
        for n in road.nodes[0]:
            self.assertIsNone(n.current_car)
        road.nodes[0][0].current_car = Car(Path([road.nodes[0][j] for j in range(1, 10)]), road.nodes[0][0], 0)
        for i in range(10):
            # Empty before the car
            for j in range(i):
                self.assertIsNone(road.nodes[0][j].current_car)
            # Check if the car is at the right place
            self.assertIsNotNone(road.nodes[0][i].current_car)
            # Empty after the car
            for j in range(i + 1, road.length):
                self.assertIsNone(road.nodes[0][j].current_car)
            road.compute_next()
            road.apply_next()

    def test_a_car_should_stop_when_there_is_a_car_ahead(self):
        simulator = Simulator()
        road = Road(simulator, 10, Orientation.NORTH, 1)
        for c in road.nodes[0]:
            self.assertIsNone(c.current_car)
        p = Path([0] * 10)
        for i in range(4, 10):
            road.nodes[0][i].current_car = Car(Path([road.nodes[0][j] for j in range(i+1, 10)]), road.nodes[0][0], 0)
        road.nodes[0][1].current_car = Car(Path([road.nodes[0][j] for j in range(2, 10)]), road.nodes[0][0], 0)

        simulator.tick()
        self.assertIsNone(road.nodes[0][1].current_car)
        self.assertIsNotNone(road.nodes[0][2].current_car)
        self.assertIsNone(road.nodes[0][3].current_car)

        simulator.tick()
        self.assertIsNone(road.nodes[0][2].current_car)
        self.assertIsNotNone(road.nodes[0][3].current_car)
        self.assertIsNotNone(road.nodes[0][4].current_car)

        simulator.tick()
        self.assertIsNone(road.nodes[0][2].current_car)
        self.assertIsNotNone(road.nodes[0][3].current_car)
        self.assertIsNotNone(road.nodes[0][4].current_car)

    def test_a_car_should_wait_before_go_forward_when_there_is_a_car_ahead(self):
        simulator = Simulator()
        road = Road(simulator, 3, Orientation.NORTH, 1)
        road.nodes[0][0].current_car = Car(Path([road.nodes[0][1], road.nodes[0][2]]), road.nodes[0][0], 0)
        road.nodes[0][1].current_car = Car(Path([road.nodes[0][2]]), road.nodes[0][1], 0)
        road.nodes[0][2].current_car = Car(Path([]), road.nodes[0][2], 0)

        simulator.tick()
        self.assertIsNotNone(road.nodes[0][0].current_car)
        self.assertIsNotNone(road.nodes[0][1].current_car)
        self.assertIsNone(road.nodes[0][2].current_car)

        simulator.tick()
        self.assertIsNotNone(road.nodes[0][0].current_car)
        self.assertIsNone(road.nodes[0][1].current_car)
        self.assertIsNotNone(road.nodes[0][2].current_car)

        simulator.tick()
        self.assertIsNone(road.nodes[0][0].current_car)
        self.assertIsNotNone(road.nodes[0][1].current_car)
        self.assertIsNone(road.nodes[0][2].current_car)

        simulator.tick()
        self.assertIsNone(road.nodes[0][0].current_car)
        self.assertIsNone(road.nodes[0][1].current_car)
        self.assertIsNotNone(road.nodes[0][2].current_car)

        simulator.tick()
        self.assertIsNone(road.nodes[0][0].current_car)
        self.assertIsNone(road.nodes[0][1].current_car)
        self.assertIsNone(road.nodes[0][2].current_car)

    def test_a_road_should_be_well_connected_when_it_has_multiple_ways(self):
        simulator = Simulator()
        road = Road(simulator, 4, Orientation.NORTH, 3)

        self.assertEqual({road.nodes[0][1], road.nodes[1][1]}, set(road.nodes[0][0].successors))
        self.assertEqual({road.nodes[0][2], road.nodes[1][2]}, set(road.nodes[0][1].successors))
        self.assertEqual({road.nodes[0][3], road.nodes[1][3]}, set(road.nodes[0][2].successors))
        self.assertEqual(set(), set(road.nodes[0][3].successors))

        self.assertEqual({road.nodes[0][1], road.nodes[1][1], road.nodes[2][1]}, set(road.nodes[1][0].successors))
        self.assertEqual({road.nodes[0][2], road.nodes[1][2], road.nodes[2][2]}, set(road.nodes[1][1].successors))
        self.assertEqual({road.nodes[0][3], road.nodes[1][3], road.nodes[2][3]}, set(road.nodes[1][2].successors))
        self.assertEqual(set(), set(road.nodes[1][3].successors))

        self.assertEqual({road.nodes[1][1], road.nodes[2][1]}, set(road.nodes[2][0].successors))
        self.assertEqual({road.nodes[1][2], road.nodes[2][2]}, set(road.nodes[2][1].successors))
        self.assertEqual({road.nodes[1][3], road.nodes[2][3]}, set(road.nodes[2][2].successors))
        self.assertEqual(set(), set(road.nodes[2][3].successors))

    def test_a_car_should_change_lane_when_the_road_has_multiple_ways(self):
        simulator = Simulator()
        road = Road(simulator, 4, Orientation.NORTH, 3)

        road.nodes[0][0].current_car = Car(Path(dijkstra_with_path(simulator.get_nodes(), simulator.weights, road.nodes[0][0], road.nodes[2][3])), road.nodes[0][0], 0)

        for _ in range(4):
            simulator.tick()

        self.assertIsNotNone(road.nodes[2][3])

    def test_a_road_should_not_be_blocked_when_cars_both_want_to_change_way(self):
        simulator = Simulator()
        road = Road(simulator, 4, Orientation.NORTH, 2)

        car1 = Car(Path([road.nodes[0][1], road.nodes[1][2], road.nodes[1][3]]), road.nodes[0][0], 0)
        car1.id = 7
        road.nodes[0][0].current_car = car1
        car2 = Car(Path([road.nodes[1][1], road.nodes[0][2], road.nodes[0][3]]), road.nodes[1][0], 0)
        car2.id = 42
        road.nodes[1][0].current_car = car2

        simulator.tick()
        self.assertEqual(car1, road.nodes[0][1].current_car)
        self.assertEqual(car2, road.nodes[1][1].current_car)

        simulator.tick()
        self.assertEqual(car1, road.nodes[0][1].current_car)
        self.assertEqual(car2, road.nodes[0][2].current_car)

        simulator.tick()
        self.assertEqual(car1, road.nodes[1][2].current_car)
        self.assertEqual(car2, road.nodes[0][3].current_car)

        simulator.tick()
        self.assertEqual(car1, road.nodes[1][3].current_car)

if __name__ == '__main__':
    unittest.main()
