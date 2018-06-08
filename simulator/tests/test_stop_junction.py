import unittest

from shared import Orientation
from simulator import Road, Simulator
from simulator.car import Car
from simulator.path import Path
from simulator.stop_junction import StopJunction
from simulator.utils import *
from copy import deepcopy


class TestStopJunction(unittest.TestCase):

    def test_car_should_stop_from_west(self):
        simulator = Simulator()
        rs = StopJunction(simulator, {Orientation.NORTH: (0, 1), Orientation.EAST: (1, 0),
                                      Orientation.SOUTH: (1, 0), Orientation.WEST: (0, 1)})
        r1 = Road(simulator, 1, Orientation.NORTH, 1)
        r2 = Road(simulator, 1, Orientation.WEST, 1)
        r3 = Road(simulator, 1, Orientation.WEST, 1)
        r1.nodes[0][0].current_car = Car(Path([rs.nodes[0][0], r3.nodes[0][0]]), r1.nodes[0][0])
        r2.nodes[0][0].current_car = Car(Path([rs.nodes[0][0], r3.nodes[0][0]]), r2.nodes[0][0])

        rs.add_predecessor(Orientation.NORTH, r1)
        rs.add_predecessor(Orientation.WEST, r2)
        r3.add_predecessor(Orientation.WEST, rs)

        print("Node", r1.nodes, r2.nodes, r3.nodes)
        print("JUNCTION", rs.nodes)
        self.assertIsNotNone(r1.nodes[0][0].current_car)
        self.assertIsNotNone(r2.nodes[0][0].current_car)
        self.assertIsNone(rs.nodes[0][0].current_car)
        self.assertIsNone(r3.nodes[0][0].current_car)

        simulator.tick()
        self.assertIsNone(r1.nodes[0][0].current_car)
        self.assertIsNotNone(r2.nodes[0][0].current_car)
        self.assertIsNotNone(rs.nodes[0][0].current_car)
        self.assertIsNone(r3.nodes[0][0].current_car)
        r1.nodes[0][0].current_car = Car(Path([rs.nodes[0][0], r3.nodes[0][0]]), r1.nodes[0][0])
        self.assertIsNotNone(r1.nodes[0][0].current_car)

        simulator.tick()
        self.assertIsNotNone(r1.nodes[0][0].current_car)
        self.assertIsNotNone(r2.nodes[0][0].current_car)
        self.assertIsNone(rs.nodes[0][0].current_car)
        self.assertIsNotNone(r3.nodes[0][0].current_car)

        simulator.tick()
        self.assertIsNone(r1.nodes[0][0].current_car)
        self.assertIsNotNone(r2.nodes[0][0].current_car)
        self.assertIsNotNone(rs.nodes[0][0].current_car)
        self.assertIsNone(r3.nodes[0][0].current_car)

        simulator.tick()
        self.assertIsNone(r1.nodes[0][0].current_car)
        self.assertIsNotNone(r2.nodes[0][0].current_car)
        self.assertIsNone(rs.nodes[0][0].current_car)
        self.assertIsNotNone(r3.nodes[0][0].current_car)

        simulator.tick()
        self.assertIsNone(r1.nodes[0][0].current_car)
        self.assertIsNone(r2.nodes[0][0].current_car)
        self.assertIsNotNone(rs.nodes[0][0].current_car)
        self.assertIsNone(r3.nodes[0][0].current_car)

    def test_car_should_stop_from_east(self):
        simulator = Simulator()
        rs = StopJunction(simulator, {Orientation.NORTH: (0, 1, False), Orientation.WEST: (1, 0, True),
                                      Orientation.SOUTH: (1, 0, False), Orientation.EAST: (0, 1, False)})
        r1 = Road(simulator, 1, Orientation.NORTH, 1)
        r2 = Road(simulator, 1, Orientation.EAST, 1)
        r3 = Road(simulator, 1, Orientation.EAST, 1)
        r1.nodes[0][0].current_car = Car(Path([rs.nodes[0][0], r3.nodes[0][0]]), r1.nodes[0][0])
        r2.nodes[0][0].current_car = Car(Path([rs.nodes[0][0], r3.nodes[0][0]]), r2.nodes[0][0])

        rs.add_predecessor(Orientation.NORTH, r1)
        rs.add_predecessor(Orientation.EAST, r2)
        r3.add_predecessor(Orientation.EAST, rs)

        self.assertIsNotNone(r1.nodes[0][0].current_car)
        self.assertIsNotNone(r2.nodes[0][0].current_car)
        self.assertIsNone(rs.nodes[0][0].current_car)
        self.assertIsNone(r3.nodes[0][0].current_car)

        simulator.tick()
        self.assertIsNone(r1.nodes[0][0].current_car)
        self.assertIsNotNone(r2.nodes[0][0].current_car)
        self.assertIsNotNone(rs.nodes[0][0].current_car)
        self.assertIsNone(r3.nodes[0][0].current_car)
        r1.nodes[0][0].current_car = Car(Path([rs.nodes[0][0], r3.nodes[0][0]]), r1.nodes[0][0])
        self.assertIsNotNone(r1.nodes[0][0].current_car)

        simulator.tick()
        self.assertIsNotNone(r1.nodes[0][0].current_car)
        self.assertIsNotNone(r2.nodes[0][0].current_car)
        self.assertIsNone(rs.nodes[0][0].current_car)
        self.assertIsNotNone(r3.nodes[0][0].current_car)

        simulator.tick()
        self.assertIsNone(r1.nodes[0][0].current_car)
        self.assertIsNotNone(r2.nodes[0][0].current_car)
        self.assertIsNotNone(rs.nodes[0][0].current_car)
        self.assertIsNone(r3.nodes[0][0].current_car)
