import unittest

from shared import Orientation
from simulator import Road, Simulator
from simulator.car import Car
from simulator.path import Path
from simulator.right_priority_junction import RightPriorityJunction
from simulator.utils import *
from copy import deepcopy


class TestRoad(unittest.TestCase):

    def test_should_go_when_there_is_no_right_priority(self):
        simulator  = Simulator()
        rp = RightPriorityJunction(simulator, 1, 1)
        r1 = Road(simulator, 1, Orientation.NORTH, 1)
        r2 = Road(simulator, 1, Orientation.WEST, 1)
        r3 = Road(simulator, 1, Orientation.EAST, 1)
        p = Path([0] * 3)
        r1.nodes[0][0].current_car = Car(p, r1.nodes[0][0])
        r2.nodes[0][0].current_car = Car(p, r2.nodes[0][0])

        rp.add_predecessor(Orientation.NORTH, r1)
        rp.add_predecessor(Orientation.WEST, r2)
        r3.add_predecessor(Orientation.EAST, rp)

        simulator.tick()
        self.assertIsNotNone(r1.nodes[0][0].current_car)
        self.assertIsNone(r2.nodes[0][0].current_car)
        self.assertIsNotNone(rp.nodes[0].current_car)
        self.assertIsNone(r3.nodes[0][0].current_car)

        simulator.tick()
        self.assertIsNotNone(r1.nodes[0][0].current_car)
        self.assertIsNone(r2.nodes[0][0].current_car)
        self.assertIsNone(rp.nodes[0].current_car)
        self.assertIsNotNone(r3.nodes[0][0].current_car)

    def test_should_go_when_there_is_right_priority_and_no_car_present(self):
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

    def test_should_not_go_when_there_is_someone_in_junction_and_no_one_in_priority_road(self):
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

    def test_should_respect_right_priority_when_there_are_3_inputs_and_an_exit_with_double_way_road(self):
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

    def test_should_respect_right_priority_when_there_are_3_inputs(self):
        rp = RightPriorityNode()
        entryN = RoadNode(Orientation.NORTH)
        entryW = RoadNode(Orientation.WEST)
        entryS = RoadNode(Orientation.SOUTH)
        exitW = RoadNode(Orientation.WEST)
        nodes = [rp, entryN, entryW, entryS, exitW]
        p = Path([0] * 3)

        entryN.current_car = Car(p, entryN)
        entryW.current_car = Car(p, entryW)
        entryS.current_car = Car(p, entryS)

        link(entryN, rp)
        link(entryW, rp)
        link(entryS, rp)
        link(rp, exitW)

        compute_next(nodes)
        apply_next(nodes)
        self.assertIsNotNone(entryN.current_car)
        self.assertIsNotNone(entryW.current_car)
        self.assertIsNone(entryS.current_car)
        self.assertIsNotNone(rp.current_car)
        self.assertIsNone(exitW.current_car)

        compute_next(nodes)
        apply_next(nodes)
        self.assertIsNotNone(entryN.current_car)
        self.assertIsNotNone(entryW.current_car)
        self.assertIsNone(entryS.current_car)
        self.assertIsNone(rp.current_car)
        self.assertIsNotNone(exitW.current_car)

        compute_next(nodes)
        apply_next(nodes)
        self.assertIsNotNone(entryN.current_car)
        self.assertIsNone(entryW.current_car)
        self.assertIsNone(entryS.current_car)
        self.assertIsNotNone(rp.current_car)
        self.assertIsNone(exitW.current_car)

    def test_should_respect_right_priority_when_there_are_2_inputs_and_2_output(self):
        rp = RightPriorityNode()
        entryN = RoadNode(Orientation.NORTH)
        entryW = RoadNode(Orientation.WEST)
        exitW = RoadNode(Orientation.WEST)
        exitN = RoadNode(Orientation.NORTH)
        nodes = [rp, entryN, entryW, exitW, exitN]

        entryW.current_car = Car(Path([0] * 3), entryW)
        entryN.current_car = Car(Path([0, 1, 0]), entryN)

        link(entryW, rp)
        link(entryN, rp)
        link(rp, exitW)
        link(rp, exitN)

        compute_next(nodes)
        apply_next(nodes)
        self.assertIsNotNone(entryN.current_car)
        self.assertIsNone(entryW.current_car)
        self.assertIsNotNone(rp.current_car)
        self.assertIsNone(exitW.current_car)
        self.assertIsNone(exitN.current_car)

        compute_next(nodes)
        apply_next(nodes)
        self.assertIsNotNone(entryN.current_car)
        self.assertIsNone(entryW.current_car)
        self.assertIsNone(rp.current_car)
        self.assertIsNotNone(exitW.current_car)
        self.assertIsNone(exitN.current_car)

        compute_next(nodes)
        apply_next(nodes)
        self.assertIsNone(entryN.current_car)
        self.assertIsNone(entryW.current_car)
        self.assertIsNotNone(rp.current_car)
        self.assertIsNone(exitW.current_car)
        self.assertIsNone(exitN.current_car)

        compute_next(nodes)
        apply_next(nodes)
        self.assertIsNone(entryN.current_car)
        self.assertIsNone(entryW.current_car)
        self.assertIsNone(rp.current_car)
        self.assertIsNone(exitW.current_car)
        self.assertIsNotNone(exitN.current_car)

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