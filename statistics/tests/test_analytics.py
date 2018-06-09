import unittest
from copy import deepcopy

from shared import Orientation
from simulator import Simulator, Entry, Exit, Path, RightPriorityJunction, Car, Road
from statistics.analytics import Analytics
from shared import dijkstra_with_path


class TestAnalytics(unittest.TestCase):

    def test_should_only_get_exit_nodes(self):
        s = Simulator()
        Entry(s, 0)
        Entry(s, 0)
        Entry(s, 0)

        exit1 = Exit(s)
        exit2 = Exit(s)

        ana = Analytics(s.entities)

        self.assertEqual({exit1: {}, exit2: {}}, ana.get_path_with_their_exit_nodes())

    def test_should_get_the_exit_nodes_with_the_travelled_path_by_the_car_which_go_through_it(self):
        simulator = Simulator()
        entry1 = Entry(simulator, 0)
        entry2 = Entry(simulator, 0)
        entry3 = Entry(simulator, 0)
        rpn = RightPriorityJunction(simulator, 1, 1)
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

        simulator.tick()
        simulator.tick()
        simulator.tick()
        simulator.tick()
        simulator.tick()
        simulator.tick()
        simulator.tick()

        ana = Analytics(simulator.entities)

        self.assertEqual({exit1: {(entry3, entry3.paths[100]): [
            [road3.nodes[0][0], road3.nodes[0][1], rpn.nodes[0][0], road4.nodes[0][0], road4.nodes[0][1]]]}},
            ana.get_path_with_their_exit_nodes())

    def test_average(self):
        s = Simulator()
        entry1 = Entry(s, 0)
        entry2 = Entry(s, 0)
        entry3 = Entry(s, 0)

        p1 = Path([0] * 6)
        p2 = Path([0] * 8)

        exit1 = Exit(s)
        exit2 = Exit(s)

        a = Analytics({})

        road1 = Road(s, 100, Orientation.SOUTH, 1)

        nodes = []

        for i in range(0, 10):
            nodes.append(road1.nodes[0][0])

        nodes1 = []

        for i in range(0, 20):
            nodes1.append(road1.nodes[0][0])

        nodes2 = []

        for i in range(0, 30):
            nodes2.append(road1.nodes[0][0])

        stats = {
            exit1: {(entry1, p1): [nodes, nodes, nodes, nodes, nodes], (entry2, p2): [nodes, nodes1, nodes1, nodes1]},
            exit2: {(entry3, p1): [nodes1, nodes, nodes2, nodes2],
                    (entry3, p2): [nodes2, nodes2, nodes2, nodes, nodes1]}}

        res = a.compute_function_per_exit(a.compute_average, stats)

        self.assertEqual({exit1: {entry1: 10, entry2: 17.5}, exit2:{entry3: 23.333333333333332}}, res)


if __name__ == '__main__':
    unittest.main()
