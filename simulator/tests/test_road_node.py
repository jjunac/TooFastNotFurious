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
            road.compute_next()
            road.apply_next()

    def test_a_car_should_stop_when_there_is_a_car_ahead(self):
        road = build_road(10, Orientation.NORTH)
        for c in road:
            self.assertIsNone(c.current_car)
        p = Path([0] * 10)
        for i in range(4, 10):
            road[i].current_car = Car(p, road[0])
        road[1].current_car = Car(p, road[0])

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
        road = build_road(3, Orientation.NORTH)
        p = Path([0] * 3)
        road[0].current_car = Car(p, road[0])
        road[1].current_car = Car(p, road[1])
        road[2].current_car = Car(p, road[2])

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

    def test_a_road_with_3_ways(self):
        e = Road(5, Orientation.NORTH, 3)
        e.link_ways()
        #first nodes of ways
        self.assertIs(e.nodes[0][0].successors[0], e.nodes[0][1])
        self.assertIs(e.nodes[0][0].successors[1], e.nodes[1][1])
        self.assertIs(e.nodes[1][0].successors[0], e.nodes[1][1])
        self.assertIs(e.nodes[1][0].successors[1], e.nodes[2][1])
        self.assertIs(e.nodes[1][0].successors[2], e.nodes[0][1])
        self.assertIs(e.nodes[2][0].successors[0], e.nodes[2][1])
        self.assertIs(e.nodes[2][0].successors[1], e.nodes[1][1])

        #last nodes of ways
        self.assertIs(e.nodes[0][3].successors[0], e.nodes[0][4])
        self.assertIs(e.nodes[0][3].successors[1], e.nodes[1][4])
        self.assertIs(e.nodes[1][3].successors[0], e.nodes[1][4])
        self.assertIs(e.nodes[1][3].successors[1], e.nodes[2][4])
        self.assertIs(e.nodes[1][3].successors[2], e.nodes[0][4])
        self.assertIs(e.nodes[2][3].successors[0], e.nodes[2][4])
        self.assertIs(e.nodes[2][3].successors[1], e.nodes[1][4])

    def test__a_road_with_1_ways(self):
        e = Road(5, Orientation.NORTH, 3)
        #first nodes of ways
        self.assertIs(e.nodes[0][0].successors[0], e.nodes[0][1])
        self.assertIs(e.nodes[0][0].successors[1], e.nodes[1][1])
        self.assertIs(e.nodes[1][0].successors[0], e.nodes[1][1])
        self.assertIs(e.nodes[1][0].successors[1], e.nodes[2][1])
        self.assertIs(e.nodes[1][0].successors[2], e.nodes[0][1])
        self.assertIs(e.nodes[2][0].successors[0], e.nodes[2][1])
        self.assertIs(e.nodes[2][0].successors[1], e.nodes[1][1])

        #last nodes of ways
        self.assertIs(e.nodes[0][3].successors[0], e.nodes[0][4])
        self.assertIs(e.nodes[0][3].successors[1], e.nodes[1][4])
        self.assertIs(e.nodes[1][3].successors[0], e.nodes[1][4])
        self.assertIs(e.nodes[1][3].successors[1], e.nodes[2][4])
        self.assertIs(e.nodes[1][3].successors[2], e.nodes[0][4])
        self.assertIs(e.nodes[2][3].successors[0], e.nodes[2][4])
        self.assertIs(e.nodes[2][3].successors[1], e.nodes[1][4])


if __name__ == '__main__':
    unittest.main()
