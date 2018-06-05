import unittest
from copy import deepcopy

from shared import Orientation
from simulator import *


class TestRoad(unittest.TestCase):

    def test_integration_3_input_1_output_with_right_priority(self):
        simulator = Simulator()
        entry1 = Entry(simulator, 0)
        entry2 = Entry(simulator, 0)
        entry3 = Entry(simulator, 0)
        entry1.to_spawn = 0
        entry2.to_spawn = 0
        entry3.to_spawn = 0

        p = Path([0] * 6)

        entry1.paths[100] = deepcopy(p)
        entry2.paths[100] = deepcopy(p)
        entry3.paths[100] = deepcopy(p)

        rpn = RightPriorityJunction(simulator, 1, 1)
        entry1.nodes[0].current_car = Car(deepcopy(p), entry1)
        entry2.nodes[0].current_car = Car(deepcopy(p), entry2)
        entry3.nodes[0].current_car = Car(deepcopy(p), entry3)

        exit1 = Exit(simulator)

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

        # Cars move from Entry to junction
        self.assertIsNotNone(entry1.nodes[0].current_car)
        self.assertIsNone(road1.nodes[0][0].current_car)
        self.assertIsNotNone(entry2.nodes[0].current_car)
        self.assertIsNone(road2.nodes[0][0].current_car)
        self.assertIsNotNone(entry3.nodes[0].current_car)
        self.assertIsNone(road3.nodes[0][0].current_car)
        simulator.tick()
        self.assertIsNone(entry1.nodes[0].current_car)
        self.assertIsNotNone(road1.nodes[0][0].current_car)
        self.assertIsNone(entry2.nodes[0].current_car)
        self.assertIsNotNone(road2.nodes[0][0].current_car)
        self.assertIsNone(entry3.nodes[0].current_car)
        self.assertIsNotNone(road3.nodes[0][0].current_car)
        simulator.tick()
        self.assertIsNone(road1.nodes[0][0].current_car)
        self.assertIsNotNone(road1.nodes[0][1].current_car)
        self.assertIsNone(road2.nodes[0][0].current_car)
        self.assertIsNotNone(road2.nodes[0][1].current_car)
        self.assertIsNone(road3.nodes[0][0].current_car)
        self.assertIsNotNone(road3.nodes[0][1].current_car)

        # Cars are going one by one in the junction
        simulator.tick()
        self.assertIsNotNone(road1.nodes[0][1].current_car)
        self.assertIsNotNone(road2.nodes[0][1].current_car)
        self.assertIsNone(road3.nodes[0][1].current_car)
        self.assertIsNotNone(rpn.nodes[0].current_car)

        simulator.tick()
        self.assertIsNotNone(road1.nodes[0][1].current_car)
        self.assertIsNotNone(road2.nodes[0][1].current_car)
        self.assertIsNone(road3.nodes[0][1].current_car)
        self.assertIsNone(rpn.nodes[0].current_car)
        self.assertIsNotNone(road4.nodes[0][0].current_car)

        simulator.tick()
        self.assertIsNotNone(road1.nodes[0][1].current_car)
        self.assertIsNone(road2.nodes[0][1].current_car)
        self.assertIsNone(road3.nodes[0][1].current_car)
        self.assertIsNotNone(rpn.nodes[0].current_car)
        self.assertIsNone(road4.nodes[0][0].current_car)
        self.assertIsNotNone(road4.nodes[0][1].current_car)

        simulator.tick()
        self.assertIsNotNone(road1.nodes[0][1].current_car)
        self.assertIsNone(road2.nodes[0][1].current_car)
        self.assertIsNone(road3.nodes[0][1].current_car)
        self.assertIsNone(rpn.nodes[0].current_car)
        self.assertIsNotNone(road4.nodes[0][0].current_car)
        self.assertIsNone(road4.nodes[0][1].current_car)
        self.assertIsNotNone(exit1.nodes[0].current_car)

        simulator.tick()
        self.assertIsNone(road1.nodes[0][1].current_car)
        self.assertIsNone(road2.nodes[0][1].current_car)
        self.assertIsNone(road3.nodes[0][1].current_car)
        self.assertIsNotNone(rpn.nodes[0].current_car)
        self.assertIsNone(road4.nodes[0][0].current_car)
        self.assertIsNotNone(road4.nodes[0][1].current_car)
        self.assertIsNone(exit1.nodes[0].current_car)

    def test_integration_2_input_2_output_with_right_priority(self):
        simulator = Simulator()
        entry1 = Entry(simulator, 0)
        entry2 = Entry(simulator, 0)
        entry1.to_spawn = 0
        entry2.to_spawn = 0

        p1 = Path([0] * 6)
        p2 = Path([0, 0, 0, 1, 0, 0])

        entry1.paths[100] = deepcopy(p1)
        entry2.paths[100] = deepcopy(p2)

        rpn = RightPriorityJunction(simulator, 1, 1)
        entry1.nodes[0].current_car = Car(deepcopy(p1), entry1)
        entry2.nodes[0].current_car = Car(deepcopy(p2), entry2)

        exit1 = Exit(simulator)
        exit2 = Exit(simulator)

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

        self.assertIsNotNone(entry1.nodes[0].current_car)
        self.assertIsNone(road1.nodes[0][0].current_car)
        self.assertIsNotNone(entry2.nodes[0].current_car)
        self.assertIsNone(road2.nodes[0][0].current_car)
        simulator.tick()
        self.assertIsNone(entry1.nodes[0].current_car)
        self.assertIsNotNone(road1.nodes[0][0].current_car)
        self.assertIsNone(entry2.nodes[0].current_car)
        self.assertIsNotNone(road2.nodes[0][0].current_car)
        simulator.tick()
        self.assertIsNone(road1.nodes[0][0].current_car)
        self.assertIsNotNone(road1.nodes[0][1].current_car)
        self.assertIsNone(road1.nodes[0][0].current_car)
        self.assertIsNotNone(road2.nodes[0][1].current_car)
        self.assertIsNone(rpn.nodes[0].current_car)

        simulator.tick()
        self.assertIsNotNone(road1.nodes[0][1].current_car)
        self.assertIsNone(road2.nodes[0][1].current_car)
        self.assertIsNotNone(rpn.nodes[0].current_car)

        simulator.tick()
        self.assertIsNotNone(road1.nodes[0][1].current_car)
        self.assertIsNone(road2.nodes[0][1].current_car)
        self.assertIsNone(rpn.nodes[0].current_car)
        self.assertIsNone(road3.nodes[0][0].current_car)
        self.assertIsNotNone(road4.nodes[0][0].current_car)

        simulator.tick()
        self.assertIsNone(road1.nodes[0][1].current_car)
        self.assertIsNone(road2.nodes[0][1].current_car)
        self.assertIsNotNone(rpn.nodes[0].current_car)
        self.assertIsNone(road3.nodes[0][0].current_car)
        self.assertIsNone(road4.nodes[0][0].current_car)

        simulator.tick()
        self.assertIsNone(road1.nodes[0][1].current_car)
        self.assertIsNone(road2.nodes[0][1].current_car)
        self.assertIsNone(rpn.nodes[0].current_car)
        self.assertIsNotNone(road3.nodes[0][0].current_car)
        self.assertIsNone(road4.nodes[0][0].current_car)

if __name__ == '__main__':
    unittest.main()
