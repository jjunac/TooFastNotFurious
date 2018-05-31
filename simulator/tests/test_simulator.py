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
        # used to prevent car to spawn randomly during integration test
        entry1.paths[100] = deepcopy(p)
        entry2.paths[100] = deepcopy(p)
        entry3.paths[100] = deepcopy(p)
        rpn = RightPriorityNode()
        entry1.current_car = Car(deepcopy(p))
        entry2.current_car = Car(deepcopy(p))
        entry3.current_car = Car(deepcopy(p))

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

        system = [entry1, entry2, entry3, exit1, rpn]
        for i in range(2):
            system.append(road1[i])
        for i in range(2):
            system.append(road2[i])
        for i in range(2):
            system.append(road3[i])
        for i in range(2):
            system.append(road4[i])

        sim = Simulator(system)

        # Cars move from Entry to junction
        self.assertIsNotNone(entry1.current_car)
        self.assertIsNone(road1[0].current_car)
        self.assertIsNotNone(entry2.current_car)
        self.assertIsNone(road2[0].current_car)
        self.assertIsNotNone(entry3.current_car)
        self.assertIsNone(road3[0].current_car)
        sim.tick()
        self.assertIsNone(entry1.current_car)
        self.assertIsNotNone(road1[0].current_car)
        self.assertIsNone(entry2.current_car)
        self.assertIsNotNone(road2[0].current_car)
        self.assertIsNone(entry3.current_car)
        self.assertIsNotNone(road3[0].current_car)
        sim.tick()
        self.assertIsNone(road1[0].current_car)
        self.assertIsNotNone(road1[1].current_car)
        self.assertIsNone(road2[0].current_car)
        self.assertIsNotNone(road2[1].current_car)
        self.assertIsNone(road3[0].current_car)
        self.assertIsNotNone(road3[1].current_car)

        #Cars are going one by one in the junction
        sim.tick()
        self.assertIsNotNone(road1[1].current_car)
        self.assertIsNotNone(road2[1].current_car)
        self.assertIsNone(road3[1].current_car)
        self.assertIsNotNone(rpn.current_car)

        sim.tick()
        self.assertIsNotNone(road1[1].current_car)
        self.assertIsNotNone(road2[1].current_car)
        self.assertIsNone(road3[1].current_car)
        self.assertIsNone(rpn.current_car)
        self.assertIsNotNone(road4[0].current_car)

        sim.tick()
        self.assertIsNotNone(road1[1].current_car)
        self.assertIsNone(road2[1].current_car)
        self.assertIsNone(road3[1].current_car)
        self.assertIsNotNone(rpn.current_car)
        self.assertIsNone(road4[0].current_car)
        self.assertIsNotNone(road4[1].current_car)

        sim.tick()
        self.assertIsNotNone(road1[1].current_car)
        self.assertIsNone(road2[1].current_car)
        self.assertIsNone(road3[1].current_car)
        self.assertIsNone(rpn.current_car)
        self.assertIsNotNone(road4[0].current_car)
        self.assertIsNone(road4[1].current_car)
        self.assertIsNotNone(exit1.current_car)

        sim.tick()
        self.assertIsNone(road1[1].current_car)
        self.assertIsNone(road2[1].current_car)
        self.assertIsNone(road3[1].current_car)
        self.assertIsNotNone(rpn.current_car)
        self.assertIsNone(road4[0].current_car)
        self.assertIsNotNone(road4[1].current_car)
        self.assertIsNone(exit1.current_car)


if __name__ == '__main__':
    unittest.main()
