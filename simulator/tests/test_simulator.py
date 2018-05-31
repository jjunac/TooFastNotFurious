import unittest
from copy import deepcopy

from simulator import EntryNode, build_road, ExitNode, Simulator, Path
from simulator.car import Car
from simulator.right_priority_node import RightPriorityNode


class TestRoad(unittest.TestCase):

    def test_integration_3_input_1_output_with_right_priority(self):
        entry1 = EntryNode(1, 1)
        entry2 = EntryNode(1, 1)
        entry3 = EntryNode(1, 1)
        entry1.to_spawn = 0
        entry2.to_spawn = 0
        entry3.to_spawn = 0

        p = Path([0] * 6)
        # used to prevent car to spawn randomly during integration test
        entry1.paths[0] = deepcopy(p)
        entry2.paths[0] = deepcopy(p)
        entry3.paths[0] = deepcopy(p)
        rpn = RightPriorityNode()
        entry1.current_car = Car(deepcopy(p))
        entry2.current_car = Car(deepcopy(p))
        entry3.current_car = Car(deepcopy(p))

        exit1 = ExitNode()

        # road to south
        road1 = build_road(2, 2)
        entry1.successors.append(road1[0])

        # road to east
        road2 = build_road(2, 1)
        entry2.successors.append(road2[0])

        # road to north
        road3 = build_road(2, 0)
        entry3.successors.append(road3[0])

        # road to east to the exit
        road4 = build_road(2, 1)
        road4[-1].successors.append(exit1)

        road1[-1].successors.append(rpn)
        road2[-1].successors.append(rpn)
        road3[-1].successors.append(rpn)
        rpn.successors.append(road4[0])
        rpn.add_priority(road1[-1], road2[-1])
        rpn.add_priority(road2[-1], road3[-1])

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
