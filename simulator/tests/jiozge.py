import unittest

from shared import Orientation
from simulator import *


class TestRoad(unittest.TestCase):

    def test_a_car_should_go_forward_when_it_is_alone(self):
        simulator = Simulator()
        road = Road(simulator, 10, Orientation.NORTH, 1)
        for n in road.nodes[0]:
            self.assertIsNone(n.current_car)
        p = Path([0] * 11)
        road.nodes[0][0].current_car = Car(p, road.nodes[0][0])
        for i in range(10):
            # Empty before the car
            for j in range(i):
                self.assertIsNone(road.nodes[0][j].current_car)
            # Check if the car is at the right place
            self.assertIsNotNone(road.nodes[0][i].current_car)
            # Empty after the car
            for j in range(i + 1, road.length):
                self.assertIsNone(road.nodes[0][j].current_car)
            simulator.tick()