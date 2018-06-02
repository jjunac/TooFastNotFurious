import unittest

from shared import Orientation
from simulator.car import Car
from simulator.path import Path
from simulator.right_priority_node import RightPriorityNode
from simulator.utils import *
from copy import deepcopy


class TestRoad(unittest.TestCase):

    def test_go_if_no_right_priority(self):
        rp = RightPriorityNode()
        r1 = RoadNode(Orientation.NORTH)
        r2 = RoadNode(Orientation.WEST)
        r3 = RoadNode(Orientation.EAST)
        nodes = [rp, r1, r2, r3]
        p = Path([0] * 3)
        r1.current_car = Car(deepcopy(p), r1)
        r2.current_car = Car(deepcopy(p), r2)

        link(r1, rp)
        link(r2, rp)
        link(rp, r3)

        compute_next(nodes)
        apply_next(nodes)
        self.assertIsNotNone(r1.current_car)
        self.assertIsNone(r2.current_car)
        self.assertIsNotNone(rp.current_car)
        self.assertIsNone(r3.current_car)

        compute_next(nodes)
        apply_next(nodes)
        self.assertIsNotNone(r1.current_car)
        self.assertIsNone(r2.current_car)
        self.assertIsNone(rp.current_car)
        self.assertIsNotNone(r3.current_car)

    def test_go_if_right_priority_and_no_car_present(self):
        rp = RightPriorityNode()
        r1 = RoadNode(Orientation.NORTH)
        r2 = RoadNode(Orientation.WEST)
        r3 = RoadNode(Orientation.EAST)
        nodes = [rp, r1, r2, r3]
        p = Path([0] * 3)
        r1.current_car = Car(deepcopy(p), r1)

        link(r1, rp)
        link(r2, rp)
        link(rp, r3)

        compute_next(nodes)
        apply_next(nodes)

        self.assertIsNone(r1.current_car)
        self.assertIsNone(r2.current_car)
        self.assertIsNotNone(rp.current_car)
        self.assertIsNone(r3.current_car)

    def test_dont_go_if_someone_in_junction_and_no_one_in_priority_road(self):
        rp = RightPriorityNode()
        r1 = RoadNode(Orientation.NORTH)
        r2 = RoadNode(Orientation.WEST)
        r3 = RoadNode(Orientation.EAST)
        nodes = [rp, r1, r2, r3]
        p = Path([0] * 3)
        r1.current_car = Car(p, r1)
        rp.current_car = Car(p, rp)

        link(r1, rp)
        link(r2, rp)
        link(rp, r3)

        compute_next(nodes)
        apply_next(nodes)
        self.assertIsNotNone(r1.current_car)
        self.assertIsNone(r2.current_car)
        self.assertIsNone(rp.current_car)
        self.assertIsNotNone(r3.current_car)

    def test_for_3_input_for_the_priority(self):
        #
        rp = RightPriorityNode()
        r1 = RoadNode(Orientation.NORTH)
        r2 = RoadNode(Orientation.WEST)
        r3 = RoadNode(Orientation.SOUTH)
        r4 = RoadNode(Orientation.EAST)
        nodes = [rp, r1, r2, r3, r4]
        p = Path([0] * 3)

        r1.current_car = Car(p, r1)
        r2.current_car = Car(p, r2)
        r3.current_car = Car(p, r3)

        link(r1, rp)
        link(r2, rp)
        link(r3, rp)
        link(rp, r4)

        compute_next(nodes)
        apply_next(nodes)
        self.assertIsNotNone(r1.current_car)
        self.assertIsNotNone(r2.current_car)
        self.assertIsNone(r3.current_car)
        self.assertIsNotNone(rp.current_car)
        self.assertIsNone(r4.current_car)

        compute_next(nodes)
        apply_next(nodes)
        self.assertIsNotNone(r1.current_car)
        self.assertIsNotNone(r2.current_car)
        self.assertIsNone(r3.current_car)
        self.assertIsNone(rp.current_car)
        self.assertIsNotNone(r4.current_car)

        compute_next(nodes)
        apply_next(nodes)
        self.assertIsNotNone(r1.current_car)
        self.assertIsNone(r2.current_car)
        self.assertIsNone(r3.current_car)
        self.assertIsNotNone(rp.current_car)
        self.assertIsNone(r4.current_car)

    def test_should_prioritize_the_car_on_the_left_of_the_exit_when_2_car_are_facing_each_others(self):
        rp = RightPriorityNode()
        entry1 = RoadNode(Orientation.EAST)
        entry2 = RoadNode(Orientation.WEST)
        exit = RoadNode(Orientation.NORTH)
        nodes = [rp, entry1, entry2, exit]
        p = Path([0] * 3)

        entry1.current_car = Car(p, entry1)
        entry2.current_car = Car(p, entry2)

        link(entry1, rp)
        link(entry2, rp)
        link(rp, exit)

        self.assertIsNotNone(entry1.current_car)
        self.assertIsNotNone(entry2.current_car)
        self.assertIsNone(exit.current_car)
        self.assertIsNone(rp.current_car)

        compute_next(nodes)
        apply_next(nodes)
        self.assertIsNotNone(entry1.current_car)
        self.assertIsNone(entry2.current_car)
        self.assertIsNone(exit.current_car)
        self.assertIsNotNone(rp.current_car)

        compute_next(nodes)
        apply_next(nodes)
        self.assertIsNotNone(entry1.current_car)
        self.assertIsNone(entry2.current_car)
        self.assertIsNotNone(exit.current_car)
        self.assertIsNone(rp.current_car)

        compute_next(nodes)
        apply_next(nodes)
        self.assertIsNone(entry1.current_car)
        self.assertIsNone(entry2.current_car)
        self.assertIsNone(exit.current_car)
        self.assertIsNotNone(rp.current_car)