import unittest
from simulator.right_priority_node import RightPriorityNode
from simulator.road_node import RoadNode



class TestRoad(unittest.TestCase):


    def test_go_if_no_right_priority(self):
        rp = RightPriorityNode()
        r1 = RoadNode()
        r1.is_car_present = True
        r2 = RoadNode()
        r2.is_car_present = True
        r3 = RoadNode()
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
        self.assertEqual(r1.is_car_present, True)
        self.assertEqual(r2.is_car_present, False)
        self.assertEqual(rp.is_car_present, True)
        self.assertEqual(r3.is_car_present, False)

        r1.compute_next()
        r2.compute_next()
        rp.compute_next()
        r3.compute_next()
        r1.apply_next()
        r2.apply_next()
        rp.apply_next()
        r3.apply_next()
        self.assertEqual(r1.is_car_present, True)
        self.assertEqual(r2.is_car_present, False)
        self.assertEqual(rp.is_car_present, False)
        self.assertEqual(r3.is_car_present, True)



    def test_go_if_right_priority_and_no_car_present(self):
        rp = RightPriorityNode()
        r1 = RoadNode()
        r1.is_car_present = True
        r2 = RoadNode()
        r2.is_car_present = False
        r3 = RoadNode()
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

        self.assertEqual(r1.next_is_car_present, False)
        self.assertEqual(r2.next_is_car_present, False)
        self.assertEqual(rp.next_is_car_present, True)
        self.assertEqual(r3.next_is_car_present, False)

    def test_dont_go_if_someone_in_junction_and_no_one_in_priority_road(self):
        rp = RightPriorityNode()
        rp.is_car_present = True
        r1 = RoadNode()
        r1.is_car_present = True
        r2 = RoadNode()
        r2.is_car_present = False
        r3 = RoadNode()
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

        self.assertEqual(r1.next_is_car_present, True)
        self.assertEqual(r2.next_is_car_present, False)
        self.assertEqual(rp.next_is_car_present, False)
        self.assertEqual(r3.next_is_car_present, True)

    def test_for_3_input_for_the_priority(self):
        rp = RightPriorityNode()
        r1 = RoadNode()
        r2 = RoadNode()
        r3 = RoadNode()
        r4 = RoadNode()
        r1.is_car_present = True
        r2.is_car_present = True
        r3.is_car_present = True

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
        self.assertEqual(r1.is_car_present, True)
        self.assertEqual(r2.is_car_present, True)
        self.assertEqual(r3.is_car_present, False)
        self.assertEqual(rp.is_car_present, True)
        self.assertEqual(r4.is_car_present, False)

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
        self.assertEqual(r1.is_car_present, True)
        self.assertEqual(r2.is_car_present, True)
        self.assertEqual(r3.is_car_present, False)
        self.assertEqual(rp.is_car_present, False)
        self.assertEqual(r4.is_car_present, True)

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
        self.assertEqual(r1.is_car_present, True)
        self.assertEqual(r2.is_car_present, False)
        self.assertEqual(r3.is_car_present, False)
        self.assertEqual(rp.is_car_present, True)
        self.assertEqual(r4.is_car_present, False)