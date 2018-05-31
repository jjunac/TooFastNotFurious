import unittest

from shared import Orientation
from simulator.car import Car
from simulator.path import Path
from simulator.right_priority_node import RightPriorityNode
from simulator.road_node import RoadNode



class TestRoad(unittest.TestCase):


    def test_go_if_no_right_priority(self):
        rp = RightPriorityNode()
        r1 = RoadNode(Orientation(0))
        r2 = RoadNode(Orientation(0))
        r3 = RoadNode(Orientation(0))
        p = Path()
        r1.current_car = Car(p)
        r2.current_car = Car(p)



        r1.successors.append(rp)
        r2.successors.append(rp)
        rp.successors.append(r3)

        rp.add_priority(r1, r2)

        r1.compute_next()
        r2.compute_next()
        rp.compute_next()
        r3.compute_next()
        r1.apply_next()
        r2.apply_next()
        rp.apply_next()
        r3.apply_next()
        self.assertIsNotNone(r1.current_car)
        self.assertIsNone(r2.current_car)
        self.assertIsNotNone(rp.current_car)
        self.assertIsNone(r3.current_car)

        r1.compute_next()
        r2.compute_next()
        rp.compute_next()
        r3.compute_next()
        r1.apply_next()
        r2.apply_next()
        rp.apply_next()
        r3.apply_next()
        self.assertIsNotNone(r1.current_car)
        self.assertIsNone(r2.current_car)
        self.assertIsNone(rp.current_car)
        self.assertIsNotNone(r3.current_car)



    def test_go_if_right_priority_and_no_car_present(self):
        rp = RightPriorityNode()
        r1 = RoadNode(Orientation(0))
        r2 = RoadNode(Orientation(0))
        r3 = RoadNode(Orientation(0))

        p = Path()
        r1.current_car = Car(p)

        r1.successors.append(rp)
        r2.successors.append(rp)
        rp.successors.append(r3)
        rp.add_priority(r1, r2)

        r1.compute_next()
        r2.compute_next()
        rp.compute_next()
        r3.compute_next()
        r1.apply_next()
        r2.apply_next()
        rp.apply_next()
        r3.apply_next()

        self.assertIsNone(r1.current_car)
        self.assertIsNone(r2.current_car)
        self.assertIsNotNone(rp.current_car)
        self.assertIsNone(r3.current_car)

    def test_dont_go_if_someone_in_junction_and_no_one_in_priority_road(self):
        rp = RightPriorityNode()
        r1 = RoadNode(Orientation(0))
        r2 = RoadNode(Orientation(0))
        r3 = RoadNode(Orientation(0))

        p = Path()
        r1.current_car = Car(p)
        rp.current_car = Car(p)

        r1.successors.append(rp)
        r2.successors.append(rp)
        rp.successors.append(r3)
        rp.add_priority(r1, r2)

        r1.compute_next()
        r2.compute_next()
        rp.compute_next()
        r3.compute_next()
        r1.apply_next()
        r2.apply_next()
        rp.apply_next()
        r3.apply_next()

        self.assertIsNotNone(r1.current_car)
        self.assertIsNone(r2.current_car)
        self.assertIsNone(rp.current_car)
        self.assertIsNotNone(r3.current_car)

    def test_for_3_input_for_the_priority(self):
        rp = RightPriorityNode()
        r1 = RoadNode(Orientation(0))
        r2 = RoadNode(Orientation(0))
        r3 = RoadNode(Orientation(0))
        r4 = RoadNode(Orientation(0))

        p = Path()
        r1.current_car = Car(p)
        r2.current_car = Car(p)
        r3.current_car = Car(p)

        r1.successors.append(rp)
        r2.successors.append(rp)
        r3.successors.append(rp)
        rp.successors.append(r4)

        rp.add_priority(r1, r2)
        rp.add_priority(r2, r3)

        r1.compute_next()
        r2.compute_next()
        r3.compute_next()
        rp.compute_next()
        r4.compute_next()
        r1.apply_next()
        r2.apply_next()
        r3.apply_next()
        rp.apply_next()
        r4.apply_next()
        self.assertIsNotNone(r1.current_car)
        self.assertIsNotNone(r2.current_car)
        self.assertIsNone(r3.current_car)
        self.assertIsNotNone(rp.current_car)
        self.assertIsNone(r4.current_car)

        r1.compute_next()
        r2.compute_next()
        r3.compute_next()
        rp.compute_next()
        r4.compute_next()
        r1.apply_next()
        r2.apply_next()
        r3.apply_next()
        rp.apply_next()
        r4.apply_next()
        self.assertIsNotNone(r1.current_car)
        self.assertIsNotNone(r2.current_car)
        self.assertIsNone(r3.current_car)
        self.assertIsNone(rp.current_car)
        self.assertIsNotNone(r4.current_car)

        r1.compute_next()
        r2.compute_next()
        r3.compute_next()
        rp.compute_next()
        r4.compute_next()
        r1.apply_next()
        r2.apply_next()
        r3.apply_next()
        rp.apply_next()
        r4.apply_next()
        self.assertIsNotNone(r1.current_car)
        self.assertIsNone(r2.current_car)
        self.assertIsNone(r3.current_car)
        self.assertIsNotNone(rp.current_car)
        self.assertIsNone(r4.current_car)