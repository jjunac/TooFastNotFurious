import unittest
from copy import deepcopy

from shared import Orientation
from simulator import Simulator, Entry, Exit, Path, RightPriorityJunction, Car, Road
from statistics.analytics import Analytics
from shared import dijkstra_with_path

class TestAnalytics(unittest.TestCase):

    def test_simple_test_get_exit_nodes(self):
        s = Simulator()
        Entry(s, 0, 1)
        Entry(s, 0, 1)
        Entry(s, 0, 1)

        exit1 = Exit(s, 1)
        exit2 = Exit(s, 1)

        ana = Analytics(s.entities)

        self.assertEqual({exit1: {}, exit2: {}}, ana.get_stats_exit_nodes())

    def test_complex_test_get_stats_exit_nodes(self):
        simulator = Simulator()
        entry1 = Entry(simulator, 0, 1)
        entry2 = Entry(simulator, 0, 1)
        entry3 = Entry(simulator, 0, 1)
        entry1.to_spawn = 0
        entry2.to_spawn = 0
        entry3.to_spawn = 0
        rpn = RightPriorityJunction(simulator, {Orientation.NORTH: (1, 0), Orientation.EAST: (0, 1), Orientation.SOUTH: (0, 1), Orientation.WEST: (1, 0)})
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

        entry1.paths[100] = Path(dijkstra_with_path(simulator.get_nodes(), entry1.nodes[0][0], exit1.nodes[0][0]))
        entry2.paths[100] = Path(dijkstra_with_path(simulator.get_nodes(), entry2.nodes[0][0], exit1.nodes[0][0]))
        entry3.paths[100] = Path(dijkstra_with_path(simulator.get_nodes(), entry3.nodes[0][0], exit1.nodes[0][0]))

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
        simulator.tick()

        ana = Analytics(simulator.entities)

        self.assertEqual({exit1: {(entry3, entry3.paths[100]): [6]}}, ana.get_stats_exit_nodes())


if __name__ == '__main__':
    unittest.main()
