import unittest
from copy import deepcopy

from shared import Orientation, dijkstra_with_path
from simulator import *


class TestRoad(unittest.TestCase):

    def test_integration_3_input_1_output_with_right_priority(self):
        simulator = Simulator()
        entry1 = Entry(simulator, 0, 1)
        entry2 = Entry(simulator, 0, 1)
        entry3 = Entry(simulator, 0, 1)
        rpn = RightPriorityJunction(simulator, {Orientation.NORTH: (1, 0), Orientation.EAST: (0, 1), Orientation.SOUTH: (1, 0), Orientation.WEST: (1, 0)})
        exit1 = Exit(simulator, 1)

        # road to south
        road1 = Road(simulator, 2, Orientation.SOUTH, 1)
        road1.add_predecessor(Orientation.SOUTH, entry1)
        rpn.add_predecessor(Orientation.SOUTH, road1)

        # road to east
        road2 = Road(simulator, 2, Orientation.EAST, 1)
        road2.add_predecessor(Orientation.EAST, entry2)
        rpn.add_predecessor(Orientation.EAST, road2)

        # road to north
        road3 = Road(simulator, 2, Orientation.NORTH, 1)
        road3.add_predecessor(Orientation.NORTH, entry3)
        rpn.add_predecessor(Orientation.NORTH, road3)

        # road to east to the exit
        road4 = Road(simulator, 2, Orientation.EAST, 1)
        exit1.add_predecessor(Orientation.EAST, road4)
        road4.add_predecessor(Orientation.EAST, rpn)

        entry1.to_spawn = 0
        entry2.to_spawn = 0
        entry3.to_spawn = 0

        p1 = Path(dijkstra_with_path(simulator.get_nodes(), entry1.nodes[0][0], exit1.nodes[0][0]))
        p2 = Path(dijkstra_with_path(simulator.get_nodes(), entry2.nodes[0][0], exit1.nodes[0][0]))
        p3 = Path(dijkstra_with_path(simulator.get_nodes(), entry3.nodes[0][0], exit1.nodes[0][0]))
        entry1.paths[100] = p1
        entry2.paths[100] = p2
        entry3.paths[100] = p3

        entry1.nodes[0][0].current_car = Car(entry1.paths[100], entry1)
        entry2.nodes[0][0].current_car = Car(entry2.paths[100], entry2)
        entry3.nodes[0][0].current_car = Car(entry3.paths[100], entry3)

        # Cars move from Entry to junction
        self.assertIsNotNone(entry1.nodes[0][0].current_car)
        self.assertIsNone(road1.nodes[0][0].current_car)
        self.assertIsNotNone(entry2.nodes[0][0].current_car)
        self.assertIsNone(road2.nodes[0][0].current_car)
        self.assertIsNotNone(entry3.nodes[0][0].current_car)
        self.assertIsNone(road3.nodes[0][0].current_car)

        self.assertEqual(0, entry1.nodes[0][0].current_car.time)
        self.assertEqual(0, entry2.nodes[0][0].current_car.time)
        self.assertEqual(0, entry3.nodes[0][0].current_car.time)

        self.assertFalse((entry1, entry1.paths[100]) in exit1.statistics.list_time_travel)
        self.assertFalse((entry2, entry2.paths[100]) in exit1.statistics.list_time_travel)
        self.assertFalse((entry3, entry3.paths[100]) in exit1.statistics.list_time_travel)

        simulator.tick()
        self.assertIsNone(entry1.nodes[0][0].current_car)
        self.assertIsNotNone(road1.nodes[0][0].current_car)
        self.assertIsNone(entry2.nodes[0][0].current_car)
        self.assertIsNotNone(road2.nodes[0][0].current_car)
        self.assertIsNone(entry3.nodes[0][0].current_car)
        self.assertIsNotNone(road3.nodes[0][0].current_car)

        self.assertEqual(1, road1.nodes[0][0].current_car.time)
        self.assertEqual(1, road2.nodes[0][0].current_car.time)
        self.assertEqual(1, road3.nodes[0][0].current_car.time)

        self.assertFalse((entry1, entry1.paths[100]) in exit1.statistics.list_time_travel)
        self.assertFalse((entry2, entry2.paths[100]) in exit1.statistics.list_time_travel)
        self.assertFalse((entry3, entry3.paths[100]) in exit1.statistics.list_time_travel)

        simulator.tick()
        self.assertIsNone(road1.nodes[0][0].current_car)
        self.assertIsNotNone(road1.nodes[0][1].current_car)
        self.assertIsNone(road2.nodes[0][0].current_car)
        self.assertIsNotNone(road2.nodes[0][1].current_car)
        self.assertIsNone(road3.nodes[0][0].current_car)
        self.assertIsNotNone(road3.nodes[0][1].current_car)

        self.assertEqual(2, road1.nodes[0][1].current_car.time)
        self.assertEqual(2, road2.nodes[0][1].current_car.time)
        self.assertEqual(2, road3.nodes[0][1].current_car.time)

        self.assertFalse((entry1, entry1.paths[100]) in exit1.statistics.list_time_travel)
        self.assertFalse((entry2, entry2.paths[100]) in exit1.statistics.list_time_travel)
        self.assertFalse((entry3, entry3.paths[100]) in exit1.statistics.list_time_travel)

        # Cars are going one by one in the junction
        simulator.tick()
        self.assertIsNotNone(road1.nodes[0][1].current_car)
        self.assertIsNotNone(road2.nodes[0][1].current_car)
        self.assertIsNone(road3.nodes[0][1].current_car)
        self.assertIsNotNone(rpn.nodes[0][0].current_car)

        self.assertEqual(3, road1.nodes[0][1].current_car.time)
        self.assertEqual(3, road2.nodes[0][1].current_car.time)
        self.assertEqual(3, rpn.nodes[0][0].current_car.time)

        self.assertFalse((entry1, entry1.paths[100]) in exit1.statistics.list_time_travel)
        self.assertFalse((entry2, entry2.paths[100]) in exit1.statistics.list_time_travel)
        self.assertFalse((entry3, entry3.paths[100]) in exit1.statistics.list_time_travel)

        simulator.tick()
        self.assertIsNotNone(road1.nodes[0][1].current_car)
        self.assertIsNotNone(road2.nodes[0][1].current_car)
        self.assertIsNone(road3.nodes[0][1].current_car)
        self.assertIsNone(rpn.nodes[0][0].current_car)
        self.assertIsNotNone(road4.nodes[0][0].current_car)

        self.assertEqual(4, road1.nodes[0][1].current_car.time)
        self.assertEqual(4, road2.nodes[0][1].current_car.time)
        self.assertEqual(4, road4.nodes[0][0].current_car.time)

        self.assertFalse((entry1, entry1.paths[100]) in exit1.statistics.list_time_travel)
        self.assertFalse((entry2, entry2.paths[100]) in exit1.statistics.list_time_travel)
        self.assertFalse((entry3, entry3.paths[100]) in exit1.statistics.list_time_travel)

        simulator.tick()
        self.assertIsNotNone(road1.nodes[0][1].current_car)
        self.assertIsNone(road2.nodes[0][1].current_car)
        self.assertIsNone(road3.nodes[0][1].current_car)
        self.assertIsNotNone(rpn.nodes[0][0].current_car)
        self.assertIsNone(road4.nodes[0][0].current_car)
        self.assertIsNotNone(road4.nodes[0][1].current_car)

        self.assertEqual(5, road1.nodes[0][1].current_car.time)
        self.assertEqual(5, road4.nodes[0][1].current_car.time)
        self.assertEqual(5, rpn.nodes[0][0].current_car.time)

        self.assertFalse((entry1, entry1.paths[100]) in exit1.statistics.list_time_travel)
        self.assertFalse((entry2, entry2.paths[100]) in exit1.statistics.list_time_travel)
        self.assertFalse((entry3, entry3.paths[100]) in exit1.statistics.list_time_travel)

        simulator.tick()
        self.assertIsNotNone(road1.nodes[0][1].current_car)
        self.assertIsNone(road2.nodes[0][1].current_car)
        self.assertIsNone(road3.nodes[0][1].current_car)
        self.assertIsNone(rpn.nodes[0][0].current_car)
        self.assertIsNotNone(road4.nodes[0][0].current_car)
        self.assertIsNone(road4.nodes[0][1].current_car)
        self.assertIsNotNone(exit1.nodes[0][0].current_car)

        self.assertEqual(6, road1.nodes[0][1].current_car.time)
        self.assertEqual(6, road4.nodes[0][0].current_car.time)
        self.assertEqual(6, exit1.nodes[0][0].current_car.time)

        self.assertFalse((entry1, entry1.paths[100]) in exit1.statistics.list_time_travel)
        self.assertFalse((entry2, entry2.paths[100]) in exit1.statistics.list_time_travel)
        self.assertFalse((entry3, entry3.paths[100]) in exit1.statistics.list_time_travel)

        simulator.tick()
        self.assertIsNone(road1.nodes[0][1].current_car)
        self.assertIsNone(road2.nodes[0][1].current_car)
        self.assertIsNone(road3.nodes[0][1].current_car)
        self.assertIsNotNone(rpn.nodes[0][0].current_car)
        self.assertIsNone(road4.nodes[0][0].current_car)
        self.assertIsNotNone(road4.nodes[0][1].current_car)
        self.assertIsNone(exit1.nodes[0][0].current_car)

        self.assertEqual(7, road4.nodes[0][1].current_car.time)
        self.assertEqual(7, rpn.nodes[0][0].current_car.time)

        self.assertFalse((entry1, entry1.paths[100]) in exit1.statistics.list_time_travel)
        self.assertFalse((entry2, entry2.paths[100]) in exit1.statistics.list_time_travel)

        self.assertTrue((entry3, entry3.paths[100]) in exit1.statistics.list_time_travel)

        self.assertEqual([6], exit1.statistics.list_time_travel[(entry3, entry3.paths[100])])

        self.assertEqual(1, len(exit1.statistics.list_time_travel))
        self.assertEqual(1, len(exit1.statistics.list_time_travel[(entry3, entry3.paths[100])]))

        self.assertEqual({(entry3, entry3.paths[100]): [6]}, exit1.get_stats())

    def test_integration_2_input_2_output_with_right_priority(self):
        simulator = Simulator()
        entry1 = Entry(simulator, 0, 1)
        entry2 = Entry(simulator, 0, 1)
        entry1.to_spawn = 0
        entry2.to_spawn = 0

        rpn = RightPriorityJunction(simulator, {Orientation.NORTH: (1, 0), Orientation.EAST: (0, 1), Orientation.SOUTH: (0, 1), Orientation.WEST: (1, 0)})
        exit1 = Exit(simulator, 1)
        exit2 = Exit(simulator, 1)

        # road to south
        road1 = Road(simulator, 2, Orientation.SOUTH, 1)
        road1.add_predecessor(Orientation.SOUTH, entry1)
        rpn.add_predecessor(Orientation.SOUTH, road1)

        # road to east
        road2 = Road(simulator, 2, Orientation.EAST, 1)
        road2.add_predecessor(Orientation.EAST, entry2)
        rpn.add_predecessor(Orientation.EAST, road2)

        # road to north
        road3 = Road(simulator, 2, Orientation.SOUTH, 1)
        exit1.add_predecessor(Orientation.SOUTH, road3)
        road3.add_predecessor(Orientation.SOUTH, rpn)

        # road to east to the exit
        road4 = Road(simulator, 2, Orientation.EAST, 1)
        exit2.add_predecessor(Orientation.SOUTH, road4)
        road4.add_predecessor(Orientation.SOUTH, rpn)

        p1 = Path(dijkstra_with_path(simulator.get_nodes(), entry1.nodes[0][0], exit1.nodes[0][0]))
        p2 = Path(dijkstra_with_path(simulator.get_nodes(), entry2.nodes[0][0], exit2.nodes[0][0]))

        entry1.paths[100] = p1
        entry2.paths[100] = p2

        entry1.nodes[0][0].current_car = Car(p1, entry1)
        entry2.nodes[0][0].current_car = Car(p2, entry2)

        self.assertIsNotNone(entry1.nodes[0][0].current_car)
        self.assertIsNone(road1.nodes[0][0].current_car)
        self.assertIsNotNone(entry2.nodes[0][0].current_car)
        self.assertIsNone(road2.nodes[0][0].current_car)
        simulator.tick()
        self.assertIsNone(entry1.nodes[0][0].current_car)
        self.assertIsNotNone(road1.nodes[0][0].current_car)
        self.assertIsNone(entry2.nodes[0][0].current_car)
        self.assertIsNotNone(road2.nodes[0][0].current_car)
        simulator.tick()
        self.assertIsNone(road1.nodes[0][0].current_car)
        self.assertIsNotNone(road1.nodes[0][1].current_car)
        self.assertIsNone(road1.nodes[0][0].current_car)
        self.assertIsNotNone(road2.nodes[0][1].current_car)
        self.assertIsNone(rpn.nodes[0][0].current_car)

        simulator.tick()
        self.assertIsNotNone(road1.nodes[0][1].current_car)
        self.assertIsNone(road2.nodes[0][1].current_car)
        self.assertIsNotNone(rpn.nodes[0][0].current_car)

        simulator.tick()
        self.assertIsNotNone(road1.nodes[0][1].current_car)
        self.assertIsNone(road2.nodes[0][1].current_car)
        self.assertIsNone(rpn.nodes[0][0].current_car)
        self.assertIsNone(road3.nodes[0][0].current_car)
        self.assertIsNotNone(road4.nodes[0][0].current_car)

        simulator.tick()
        self.assertIsNone(road1.nodes[0][1].current_car)
        self.assertIsNone(road2.nodes[0][1].current_car)
        self.assertIsNotNone(rpn.nodes[0][0].current_car)
        self.assertIsNone(road3.nodes[0][0].current_car)
        self.assertIsNone(road4.nodes[0][0].current_car)

        simulator.tick()
        self.assertIsNone(road1.nodes[0][1].current_car)
        self.assertIsNone(road2.nodes[0][1].current_car)
        self.assertIsNone(rpn.nodes[0][0].current_car)
        self.assertIsNotNone(road3.nodes[0][0].current_car)
        self.assertIsNone(road4.nodes[0][0].current_car)


if __name__ == '__main__':
    unittest.main()
