import unittest

from engine.road_node import RoadNode
from engine.utils import *


class MyTestCase(unittest.TestCase):

    def test_a_car_should_go_forward_when_it_is_alone(self):
        road = build_road(10)
        for n in road:
            self.assertFalse(n.is_car_present)
        road[0].is_car_present = True
        for i in range(10):
            # Empty before the car
            for j in range(i):
                self.assertFalse(road[j].is_car_present)
            # Check if the car is at the right place
            self.assertTrue(road[i].is_car_present)
            # Empty after the car
            for j in range(i+1, len(road)):
                self.assertFalse(road[j].is_car_present)
            compute_next(road)
            apply_next(road)


    def test_a_car_should_stop_when_there_is_a_car_ahead(self):
        road = build_road(10)
        for c in road:
            self.assertFalse(False, c.is_car_present)
        for i in range(4, 10):
            road[i].is_car_present = True
        road[1].is_car_present = True

        compute_next(road)
        apply_next(road)
        self.assertFalse(road[1].is_car_present)
        self.assertTrue(road[2].is_car_present)
        self.assertFalse(road[3].is_car_present)

        compute_next(road)
        apply_next(road)
        self.assertFalse(road[2].is_car_present)
        self.assertTrue(road[3].is_car_present)
        self.assertTrue(road[4].is_car_present)

        compute_next(road)
        apply_next(road)
        self.assertFalse(road[2].is_car_present)
        self.assertTrue(road[3].is_car_present)
        self.assertTrue(road[4].is_car_present)

    def test_a_car_should_wait_before_go_forward_when_there_is_a_car_ahead(self):
        road = build_road(3)
        road[0].is_car_present = True
        road[1].is_car_present = True
        road[2].is_car_present = True

        compute_next(road)
        apply_next(road)
        self.assertTrue(road[0].is_car_present)
        self.assertTrue(road[1].is_car_present)
        self.assertFalse(road[2].is_car_present)

        compute_next(road)
        apply_next(road)
        self.assertTrue(road[0].is_car_present)
        self.assertFalse(road[1].is_car_present)
        self.assertTrue(road[2].is_car_present)

        compute_next(road)
        apply_next(road)
        self.assertFalse(road[0].is_car_present)
        self.assertTrue(road[1].is_car_present)
        self.assertFalse(road[2].is_car_present)

        compute_next(road)
        apply_next(road)
        self.assertFalse(road[0].is_car_present)
        self.assertFalse(road[1].is_car_present)
        self.assertTrue(road[2].is_car_present)

        compute_next(road)
        apply_next(road)
        self.assertFalse(road[0].is_car_present)
        self.assertFalse(road[1].is_car_present)
        self.assertFalse(road[2].is_car_present)


if __name__ == '__main__':
    unittest.main()
