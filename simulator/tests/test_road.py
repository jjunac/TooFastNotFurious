import unittest

from shared import Orientation
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
        road.nodes[0][0].current_car = Car(Path([road.nodes[0][j] for j in range(1, 10)]), road.nodes[0][0])
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
            road.nodes[0][i].current_car = Car(Path([road.nodes[0][j] for j in range(i+1, 10)]), road.nodes[0][0])
        road.nodes[0][1].current_car = Car(Path([road.nodes[0][j] for j in range(2, 10)]), road.nodes[0][0])

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
        road.nodes[0][0].current_car = Car(Path([road.nodes[0][1], road.nodes[0][2]]), road.nodes[0][0])
        road.nodes[0][1].current_car = Car(Path([road.nodes[0][2]]), road.nodes[0][1])
        road.nodes[0][2].current_car = Car(Path([]), road.nodes[0][2])

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

if __name__ == '__main__':
    unittest.main()
