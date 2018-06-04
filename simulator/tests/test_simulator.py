import unittest
from copy import deepcopy

from shared import Orientation
from simulator import *


class TestRoad(unittest.TestCase):

    def test_integration_3_input_1_output_with_right_priority(self):
        entry1 = EntryNode(1, 0)
        entry2 = EntryNode(1, 0)
        entry3 = EntryNode(1, 0)
        entry1.to_spawn = 0
        entry2.to_spawn = 0
        entry3.to_spawn = 0

        p = Path([0] * 6)

        entry1.paths[100] = deepcopy(p)
        entry2.paths[100] = deepcopy(p)
        entry3.paths[100] = deepcopy(p)
        rpn = RightPriorityNode()
        entry1.current_car = Car(p, entry1)
        entry2.current_car = Car(p, entry2)
        entry3.current_car = Car(p, entry3)

        exit1 = ExitNode()

        # road to south
        road1 = build_road(2, Orientation.SOUTH)
        link(entry1, road1[0])

        # road to east
        road2 = build_road(2, Orientation.EAST)
        link(entry2, road2[0])

        # road to north
        road3 = build_road(2, Orientation.NORTH)
        link(entry3, road3[0])

        # road to east to the exit
        road4 = build_road(2, 1)
        link(road4[-1], exit1)

        link(road1[-1], rpn)
        link(road2[-1], rpn)
        link(road3[-1], rpn)
        link(rpn, road4[0])

        system = [entry1, entry2, entry3, exit1, rpn, *road1, *road2, *road3, *road4]

        sim = Simulator(system)

        # Cars move from Entry to junction
        self.assertIsNotNone(entry1.current_car)
        self.assertIsNone(road1[0].current_car)
        self.assertIsNotNone(entry2.current_car)
        self.assertIsNone(road2[0].current_car)
        self.assertIsNotNone(entry3.current_car)
        self.assertIsNone(road3[0].current_car)

        self.assertEqual(0, entry1.current_car.time)
        self.assertEqual(0, entry2.current_car.time)
        self.assertEqual(0, entry3.current_car.time)

        self.assertFalse(p in exit1.statistics.list_time_travel)

        sim.tick()
        self.assertIsNone(entry1.current_car)
        self.assertIsNotNone(road1[0].current_car)
        self.assertIsNone(entry2.current_car)
        self.assertIsNotNone(road2[0].current_car)
        self.assertIsNone(entry3.current_car)
        self.assertIsNotNone(road3[0].current_car)

        self.assertEqual(1, road1[0].current_car.time)
        self.assertEqual(1, road2[0].current_car.time)
        self.assertEqual(1, road3[0].current_car.time)

        self.assertFalse(p in exit1.statistics.list_time_travel)

        sim.tick()
        self.assertIsNone(road1[0].current_car)
        self.assertIsNotNone(road1[1].current_car)
        self.assertIsNone(road2[0].current_car)
        self.assertIsNotNone(road2[1].current_car)
        self.assertIsNone(road3[0].current_car)
        self.assertIsNotNone(road3[1].current_car)

        self.assertEqual(2, road1[1].current_car.time)
        self.assertEqual(2, road2[1].current_car.time)
        self.assertEqual(2, road3[1].current_car.time)

        self.assertFalse(p in exit1.statistics.list_time_travel)

        # Cars are going one by one in the junction
        sim.tick()
        self.assertIsNotNone(road1[1].current_car)
        self.assertIsNotNone(road2[1].current_car)
        self.assertIsNone(road3[1].current_car)
        self.assertIsNotNone(rpn.current_car)

        self.assertEqual(3, road1[1].current_car.time)
        self.assertEqual(3, road2[1].current_car.time)
        self.assertEqual(3, rpn.current_car.time)

        self.assertFalse(p in exit1.statistics.list_time_travel)

        sim.tick()
        self.assertIsNotNone(road1[1].current_car)
        self.assertIsNotNone(road2[1].current_car)
        self.assertIsNone(road3[1].current_car)
        self.assertIsNone(rpn.current_car)
        self.assertIsNotNone(road4[0].current_car)

        self.assertEqual(4, road1[1].current_car.time)
        self.assertEqual(4, road2[1].current_car.time)
        self.assertEqual(4, road4[0].current_car.time)

        self.assertFalse(p in exit1.statistics.list_time_travel)

        sim.tick()
        self.assertIsNotNone(road1[1].current_car)
        self.assertIsNone(road2[1].current_car)
        self.assertIsNone(road3[1].current_car)
        self.assertIsNotNone(rpn.current_car)
        self.assertIsNone(road4[0].current_car)
        self.assertIsNotNone(road4[1].current_car)

        self.assertEqual(5, road1[1].current_car.time)
        self.assertEqual(5, road4[1].current_car.time)
        self.assertEqual(5, rpn.current_car.time)

        self.assertFalse(p in exit1.statistics.list_time_travel)

        sim.tick()
        self.assertIsNotNone(road1[1].current_car)
        self.assertIsNone(road2[1].current_car)
        self.assertIsNone(road3[1].current_car)
        self.assertIsNone(rpn.current_car)
        self.assertIsNotNone(road4[0].current_car)
        self.assertIsNone(road4[1].current_car)
        self.assertIsNotNone(exit1.current_car)

        self.assertEqual(6, road1[1].current_car.time)
        self.assertEqual(6, road4[0].current_car.time)
        self.assertEqual(6, exit1.current_car.time)

        self.assertFalse(p in exit1.statistics.list_time_travel)

        sim.tick()
        self.assertIsNone(road1[1].current_car)
        self.assertIsNone(road2[1].current_car)
        self.assertIsNone(road3[1].current_car)
        self.assertIsNotNone(rpn.current_car)
        self.assertIsNone(road4[0].current_car)
        self.assertIsNotNone(road4[1].current_car)
        self.assertIsNone(exit1.current_car)

        self.assertEqual(7, road4[1].current_car.time)
        self.assertEqual(7, rpn.current_car.time)

        self.assertTrue(p in exit1.statistics.list_time_travel)

        self.assertEqual(6, exit1.statistics.list_time_travel[p][0])
        self.assertEqual(1, len(exit1.statistics.list_time_travel))
        self.assertEqual(1, len(exit1.statistics.list_time_travel[p]))

        self.assertEqual({p: [6]}, exit1.get_stats())
        self.assertEqual({exit1: {p: [6]}}, sim.get_stats())

    def test_integration_2_input_2_output_with_right_priority(self):
        entry1 = EntryNode(1, 0)
        entry2 = EntryNode(1, 0)
        entry1.to_spawn = 0
        entry2.to_spawn = 0

        p1 = Path([0] * 6)
        p2 = Path([0, 0, 0, 1, 0, 0])

        # used to prevent car to spawn randomly during integration test
        entry1.paths[100] = deepcopy(p1)
        entry2.paths[100] = deepcopy(p2)

        rpn = RightPriorityNode()
        entry1.current_car = Car(deepcopy(p1), entry1)
        entry2.current_car = Car(deepcopy(p2), entry2)

        exit1 = ExitNode()
        exit2 = ExitNode()

        # road to south
        road1 = build_road(2, Orientation.SOUTH)
        link(entry1, road1[0])

        # road to east
        road2 = build_road(2, Orientation.EAST)
        link(entry2, road2[0])

        # road to north
        road3 = build_road(2, Orientation.SOUTH)
        link(road3[-1], exit1)

        # road to east to the exit
        road4 = build_road(2, Orientation.EAST)
        link(road4[-1], exit2)

        link(road1[-1], rpn)
        link(road2[-1], rpn)
        link(rpn, road3[0])
        link(rpn, road4[0])

        system = [entry1, entry2, exit1, exit2, rpn, *road1, *road2, *road3, *road4]

        sim = Simulator(system)
        self.assertIsNotNone(entry1.current_car)
        self.assertIsNone(road1[0].current_car)
        self.assertIsNotNone(entry2.current_car)
        self.assertIsNone(road2[0].current_car)
        sim.tick()
        self.assertIsNone(entry1.current_car)
        self.assertIsNotNone(road1[0].current_car)
        self.assertIsNone(entry2.current_car)
        self.assertIsNotNone(road2[0].current_car)
        sim.tick()
        self.assertIsNone(road1[0].current_car)
        self.assertIsNotNone(road1[1].current_car)
        self.assertIsNone(road1[0].current_car)
        self.assertIsNotNone(road2[1].current_car)
        self.assertIsNone(rpn.current_car)

        sim.tick()
        self.assertIsNotNone(road1[1].current_car)
        self.assertIsNone(road2[1].current_car)
        self.assertIsNotNone(rpn.current_car)

        sim.tick()
        self.assertIsNotNone(road1[1].current_car)
        self.assertIsNone(road2[1].current_car)
        self.assertIsNone(rpn.current_car)
        self.assertIsNone(road3[0].current_car)
        self.assertIsNotNone(road4[0].current_car)

        sim.tick()
        self.assertIsNone(road1[1].current_car)
        self.assertIsNone(road2[1].current_car)
        self.assertIsNotNone(rpn.current_car)
        self.assertIsNone(road3[0].current_car)
        self.assertIsNone(road4[0].current_car)

        sim.tick()
        self.assertIsNone(road1[1].current_car)
        self.assertIsNone(road2[1].current_car)
        self.assertIsNone(rpn.current_car)
        self.assertIsNotNone(road3[0].current_car)
        self.assertIsNone(road4[0].current_car)

        self.assertEqual({exit1: {}, exit2: {}}, sim.get_stats())


if __name__ == '__main__':
    unittest.main()
