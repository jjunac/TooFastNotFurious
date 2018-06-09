import unittest

from shared import Orientation
from simulator import Road, Simulator
from simulator.car import Car
from simulator.path import Path
from simulator.stop_junction import StopJunction
from simulator.utils import *
from copy import deepcopy


class TestStopJunction(unittest.TestCase):

    def test_a_car_should_leave_priority_when_it_is_at_a_stop_and_there_is_another_car_on_the_right(self):
        simulator = Simulator()
        stop = StopJunction(simulator, {Orientation.NORTH: (0, 1), Orientation.EAST: (1, 0),
                                      Orientation.SOUTH: (1, 0), Orientation.WEST: (0, 1)}, Orientation.WEST)
        r1 = Road(simulator, 1, Orientation.NORTH, 1)
        r2 = Road(simulator, 1, Orientation.WEST, 1)
        r3 = Road(simulator, 1, Orientation.WEST, 1)
        r1.nodes[0][0].current_car = Car(Path([stop.nodes[0][0], r3.nodes[0][0]]), r1.nodes[0][0])
        r2.nodes[0][0].current_car = Car(Path([stop.nodes[0][0], r3.nodes[0][0]]), r2.nodes[0][0])

        stop.add_predecessor(Orientation.NORTH, r1)
        stop.add_predecessor(Orientation.WEST, r2)
        r3.add_predecessor(Orientation.WEST, stop)

        self.assertIsNotNone(r1.nodes[0][0].current_car)
        self.assertIsNotNone(r2.nodes[0][0].current_car)
        self.assertIsNone(stop.nodes[0][0].current_car)
        self.assertIsNone(r3.nodes[0][0].current_car)

        simulator.tick()
        self.assertIsNone(r1.nodes[0][0].current_car)
        self.assertIsNotNone(r2.nodes[0][0].current_car)
        self.assertIsNotNone(stop.nodes[0][0].current_car)
        self.assertIsNone(r3.nodes[0][0].current_car)

        simulator.tick()
        self.assertIsNone(r1.nodes[0][0].current_car)
        self.assertIsNotNone(r2.nodes[0][0].current_car)
        self.assertIsNone(stop.nodes[0][0].current_car)
        self.assertIsNotNone(r3.nodes[0][0].current_car)

        simulator.tick()
        self.assertIsNone(r1.nodes[0][0].current_car)
        self.assertIsNone(r2.nodes[0][0].current_car)
        self.assertIsNotNone(stop.nodes[0][0].current_car)
        self.assertIsNone(r3.nodes[0][0].current_car)


    def test_a_car_should_leave_priority_when_it_is_at_a_stop_and_there_is_another_car_on_the_left(self):
        simulator = Simulator()
        stop = StopJunction(simulator, {Orientation.NORTH: (0, 1), Orientation.EAST: (0, 1),
                                      Orientation.SOUTH: (1, 0), Orientation.WEST: (1, 0)}, Orientation.EAST)
        r1 = Road(simulator, 1, Orientation.NORTH, 1)
        r2 = Road(simulator, 1, Orientation.EAST, 1)
        r3 = Road(simulator, 1, Orientation.EAST, 1)
        r1.nodes[0][0].current_car = Car(Path([stop.nodes[0][0], r3.nodes[0][0]]), r1.nodes[0][0])
        r2.nodes[0][0].current_car = Car(Path([stop.nodes[0][0], r3.nodes[0][0]]), r2.nodes[0][0])

        stop.add_predecessor(Orientation.NORTH, r1)
        stop.add_predecessor(Orientation.EAST, r2)
        r3.add_predecessor(Orientation.EAST, stop)

        self.assertIsNotNone(r1.nodes[0][0].current_car)
        self.assertIsNotNone(r2.nodes[0][0].current_car)
        self.assertIsNone(stop.nodes[0][0].current_car)
        self.assertIsNone(r3.nodes[0][0].current_car)

        simulator.tick()
        self.assertIsNone(r1.nodes[0][0].current_car)
        self.assertIsNotNone(r2.nodes[0][0].current_car)
        self.assertIsNotNone(stop.nodes[0][0].current_car)
        self.assertIsNone(r3.nodes[0][0].current_car)

        simulator.tick()
        self.assertIsNone(r1.nodes[0][0].current_car)
        self.assertIsNotNone(r2.nodes[0][0].current_car)
        self.assertIsNone(stop.nodes[0][0].current_car)
        self.assertIsNotNone(r3.nodes[0][0].current_car)

        simulator.tick()
        self.assertIsNone(r1.nodes[0][0].current_car)
        self.assertIsNone(r2.nodes[0][0].current_car)
        self.assertIsNotNone(stop.nodes[0][0].current_car)
        self.assertIsNone(r3.nodes[0][0].current_car)

    def test_a_car_should_leave_priority_when_it_is_at_a_stop_and_there_are_another_cars_on_the_left_and_on_the_right(self):
        simulator = Simulator()
        stop = StopJunction(simulator, {Orientation.NORTH: (1, 0), Orientation.EAST: (0, 1),
                                      Orientation.SOUTH: (1, 0), Orientation.WEST: (1, 0)}, Orientation.EAST)
        r1 = Road(simulator, 1, Orientation.NORTH, 1)
        r2 = Road(simulator, 1, Orientation.EAST, 1)
        r3 = Road(simulator, 1, Orientation.SOUTH, 1)
        r4 = Road(simulator, 1, Orientation.EAST, 1)

        r1.nodes[0][0].current_car = Car(Path([stop.nodes[0][0], r4.nodes[0][0]]), r1.nodes[0][0])
        r2.nodes[0][0].current_car = Car(Path([stop.nodes[0][0], r4.nodes[0][0]]), r2.nodes[0][0])
        r3.nodes[0][0].current_car = Car(Path([stop.nodes[0][0], r4.nodes[0][0]]), r3.nodes[0][0])

        stop.add_predecessor(Orientation.NORTH, r1)
        stop.add_predecessor(Orientation.EAST, r2)
        stop.add_predecessor(Orientation.SOUTH, r3)
        r4.add_predecessor(Orientation.EAST, stop)

        self.assertIsNotNone(r1.nodes[0][0].current_car)
        self.assertIsNotNone(r2.nodes[0][0].current_car)
        self.assertIsNotNone(r3.nodes[0][0].current_car)
        self.assertIsNone(stop.nodes[0][0].current_car)
        self.assertIsNone(r4.nodes[0][0].current_car)

        simulator.tick()
        self.assertIsNone(r1.nodes[0][0].current_car)
        self.assertIsNotNone(r2.nodes[0][0].current_car)
        self.assertIsNotNone(r3.nodes[0][0].current_car)
        self.assertIsNotNone(stop.nodes[0][0].current_car)
        self.assertIsNone(r4.nodes[0][0].current_car)

        simulator.tick()
        self.assertIsNone(r1.nodes[0][0].current_car)
        self.assertIsNotNone(r2.nodes[0][0].current_car)
        self.assertIsNotNone(r3.nodes[0][0].current_car)
        self.assertIsNone(stop.nodes[0][0].current_car)
        self.assertIsNotNone(r4.nodes[0][0].current_car)

        simulator.tick()
        self.assertIsNone(r1.nodes[0][0].current_car)
        self.assertIsNotNone(r2.nodes[0][0].current_car)
        self.assertIsNone(r3.nodes[0][0].current_car)
        self.assertIsNotNone(stop.nodes[0][0].current_car)
        self.assertIsNone(r4.nodes[0][0].current_car)

        simulator.tick()
        self.assertIsNone(r1.nodes[0][0].current_car)
        self.assertIsNotNone(r2.nodes[0][0].current_car)
        self.assertIsNone(r3.nodes[0][0].current_car)
        self.assertIsNone(stop.nodes[0][0].current_car)
        self.assertIsNotNone(r4.nodes[0][0].current_car)

        simulator.tick()
        self.assertIsNone(r1.nodes[0][0].current_car)
        self.assertIsNone(r2.nodes[0][0].current_car)
        self.assertIsNone(r3.nodes[0][0].current_car)
        self.assertIsNotNone(stop.nodes[0][0].current_car)
        self.assertIsNone(r4.nodes[0][0].current_car)