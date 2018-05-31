import unittest

from shared import Orientation
from simulator.car import Car
from simulator.path import Path
from simulator.utils import *


class MyTestCase(unittest.TestCase):

    def test_a_car_should_go_forward_when_it_is_alone(self):
        road = build_road(10, Orientation.NORTH)
        for n in road:
            self.assertIsNone(n.current_car)
        p = Path([0] * 11)
        road[0].current_car = Car(p)
        for i in range(10):
            # Empty before the car
            for j in range(i):
                self.assertIsNone(road[j].current_car)
            # Check if the car is at the right place
            self.assertIsNotNone(road[i].current_car)
            # Empty after the car
            for j in range(i + 1, len(road)):
                self.assertIsNone(road[j].current_car)
            compute_next(road)
            apply_next(road)

    def test_a_car_should_stop_when_there_is_a_car_ahead(self):
        road = build_road(10,Orientation(0))
        for c in road:
            self.assertIsNone(c.current_car)
        p = Path
        for i in range(4, 10):
            road[i].current_car = Car(p)
        road[1].current_car = Car(p)

        compute_next(road)
        apply_next(road)
        self.assertIsNone(road[1].current_car)
        self.assertIsNotNone(road[2].current_car)
        self.assertIsNone(road[3].current_car)

        compute_next(road)
        apply_next(road)
        self.assertIsNone(road[2].current_car)
        self.assertIsNotNone(road[3].current_car)
        self.assertIsNotNone(road[4].current_car)

        compute_next(road)
        apply_next(road)
        self.assertIsNone(road[2].current_car)
        self.assertIsNotNone(road[3].current_car)
        self.assertIsNotNone(road[4].current_car)

    def test_a_car_should_wait_before_go_forward_when_there_is_a_car_ahead(self):
        road = build_road(3, Orientation(0))
        p = Path
        road[0].current_car = Car(p)
        road[1].current_car = Car(p)
        road[2].current_car = Car(p)

        compute_next(road)
        apply_next(road)
        self.assertIsNotNone(road[0].current_car)
        self.assertIsNotNone(road[1].current_car)
        self.assertIsNone(road[2].current_car)

        compute_next(road)
        apply_next(road)
        self.assertIsNotNone(road[0].current_car)
        self.assertIsNone(road[1].current_car)
        self.assertIsNotNone(road[2].current_car)

        compute_next(road)
        apply_next(road)
        self.assertIsNone(road[0].current_car)
        self.assertIsNotNone(road[1].current_car)
        self.assertIsNone(road[2].current_car)

        compute_next(road)
        apply_next(road)
        self.assertIsNone(road[0].current_car)
        self.assertIsNone(road[1].current_car)
        self.assertIsNotNone(road[2].current_car)

        compute_next(road)
        apply_next(road)
        self.assertIsNone(road[0].current_car)
        self.assertIsNone(road[1].current_car)
        self.assertIsNone(road[2].current_car)


if __name__ == '__main__':
    unittest.main()
