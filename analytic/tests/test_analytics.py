import unittest
from copy import deepcopy

from shared import Orientation
from simulator import Simulator, Entry, Exit, Path, RightPriorityJunction, Car, Road
from analytic.analytics import Analytics
from shared import dijkstra_with_path


class TestAnalytics(unittest.TestCase):

    def test_should_only_get_exit_nodes(self):
        s = Simulator()
        Entry(s, 0, 1)
        Entry(s, 0, 1)
        Entry(s, 0, 1)

        exit1 = Exit(s, 1)
        exit2 = Exit(s, 1)

        ana = Analytics(s.entities, [])

        self.assertEqual({exit1: {}, exit2: {}}, ana.get_path_with_their_exit_nodes())

    def test_should_get_the_exit_nodes_with_the_travelled_path_by_the_car_which_go_through_it(self):
        simulator = Simulator()
        entry1 = Entry(simulator, 0, 1)
        entry2 = Entry(simulator, 0, 1)
        entry3 = Entry(simulator, 0, 1)
        rpn = RightPriorityJunction(simulator,
                                    {Orientation.NORTH: (1, 0), Orientation.EAST: (0, 1), Orientation.SOUTH: (1, 0),
                                     Orientation.WEST: (1, 0)})
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

        p1 = Path(dijkstra_with_path(simulator.get_nodes(), simulator.weights, entry1.nodes[0][0], exit1.nodes[0][0]))
        p2 = Path(dijkstra_with_path(simulator.get_nodes(), simulator.weights, entry2.nodes[0][0], exit1.nodes[0][0]))
        p3 = Path(dijkstra_with_path(simulator.get_nodes(), simulator.weights, entry3.nodes[0][0], exit1.nodes[0][0]))
        entry1.paths[100] = p1
        entry2.paths[100] = p2
        entry3.paths[100] = p3

        car1 = Car(entry1.paths[100], entry1, 0)
        car2 = Car(entry2.paths[100], entry2, 0)
        car3 = Car(entry3.paths[100], entry3, 0)

        entry1.nodes[0][0].current_car = car1
        entry2.nodes[0][0].current_car = car2
        entry3.nodes[0][0].current_car = car3

        simulator.tick()
        simulator.tick()
        simulator.tick()
        simulator.tick()
        simulator.tick()
        simulator.tick()
        simulator.tick()

        ana = Analytics(simulator.entities, [])

        self.assertEqual({exit1: {(entry3, entry3.paths[100]): [car3]}},
                         ana.get_path_with_their_exit_nodes())

        self.assertEqual([road3.nodes[0][0], road3.nodes[0][1], rpn.nodes[0][0], road4.nodes[0][0], road4.nodes[0][1]],
                         ana.get_path_with_their_exit_nodes()[exit1][(entry3, entry3.paths[100])][0].visited_nodes)

    def test_should_compute_average_for_exit_nodes(self):
        s = Simulator()
        entry1 = Entry(s, 0, 1)
        entry2 = Entry(s, 0, 1)
        entry3 = Entry(s, 0, 1)

        p1 = Path([])
        p2 = Path([])

        exit1 = Exit(s, 1)
        exit2 = Exit(s, 1)

        a = Analytics({}, [])

        road1 = Road(s, 100, Orientation.SOUTH, 1)

        car1 = Car(p2, entry1, 0)
        car2 = Car(p2, entry2, 0)
        car3 = Car(p2, entry3, 0)

        nodes = []

        for i in range(0, 10):
            nodes.append(road1.nodes[0][i])

        car1.visited_nodes = nodes

        nodes1 = []

        for i in range(0, 20):
            nodes1.append(road1.nodes[0][i])

        car2.visited_nodes = nodes1

        nodes2 = []

        for i in range(0, 30):
            nodes2.append(road1.nodes[0][i])

        car3.visited_nodes = nodes2

        stats = {
            exit1: {(entry1, p1): [car1, car1, car1, car1, car1], (entry2, p2): [car2, car1, car2, car2]},
            exit2: {(entry3, p1): [car2, car1, car3, car3],
                    (entry3, p2): [car3, car3, car3, car1, car2]}}

        res = a.compute_function_per_exit(stats)

        self.assertTrue(exit1 in res[0])
        self.assertTrue(exit2 in res[0])
        self.assertTrue(entry1 in res[0][exit1])
        self.assertTrue(entry2 in res[0][exit1])
        self.assertTrue(entry3 in res[0][exit2])
        self.assertEqual(10, res[0][exit1][entry1])
        self.assertEqual(17.5, res[0][exit1][entry2])
        self.assertAlmostEqual(23.33, res[0][exit2][entry3], delta=0.1)

    def test_should_compute_first_quartile_for_exit_nodes(self):
        s = Simulator()
        entry1 = Entry(s, 0, 1)
        entry2 = Entry(s, 0, 1)
        entry3 = Entry(s, 0, 1)

        p1 = Path([])
        p2 = Path([])

        exit1 = Exit(s, 1)
        exit2 = Exit(s, 1)

        a = Analytics({}, [])

        road1 = Road(s, 100, Orientation.SOUTH, 1)

        car1 = Car(p2, entry1, 0)
        car2 = Car(p2, entry2, 0)
        car3 = Car(p2, entry3, 0)

        nodes = []

        for i in range(0, 10):
            nodes.append(road1.nodes[0][i])

        car1.visited_nodes = nodes

        nodes1 = []

        for i in range(0, 20):
            nodes1.append(road1.nodes[0][i])

        car2.visited_nodes = nodes1

        nodes2 = []

        for i in range(0, 30):
            nodes2.append(road1.nodes[0][i])

        car3.visited_nodes = nodes2

        stats = {
            exit1: {(entry1, p1): [car1, car1, car1, car1, car1], (entry2, p2): [car2, car1, car2, car2]},
            exit2: {(entry3, p1): [car2, car1, car3, car3],
                    (entry3, p2): [car3, car3, car3, car1, car2]}}

        res = a.compute_function_per_exit(stats)

        self.assertEqual({exit1: {entry1: 10, entry2: 10}, exit2: {entry3: 20}}, res[2])

    def test_should_compute_third_quartile_for_exit_nodes(self):
        s = Simulator()
        entry1 = Entry(s, 0, 1)
        entry2 = Entry(s, 0, 1)
        entry3 = Entry(s, 0, 1)

        p1 = Path([])
        p2 = Path([])

        exit1 = Exit(s, 1)
        exit2 = Exit(s, 1)

        a = Analytics({}, [])

        road1 = Road(s, 100, Orientation.SOUTH, 1)

        car1 = Car(p2, entry1, 0)
        car2 = Car(p2, entry2, 0)
        car3 = Car(p2, entry3, 0)

        nodes = []

        for i in range(0, 10):
            nodes.append(road1.nodes[0][i])

        car1.visited_nodes = nodes

        nodes1 = []

        for i in range(0, 20):
            nodes1.append(road1.nodes[0][i])

        car2.visited_nodes = nodes1

        nodes2 = []

        for i in range(0, 30):
            nodes2.append(road1.nodes[0][i])

        car3.visited_nodes = nodes2
        stats = {
            exit1: {(entry1, p1): [car1, car1, car1, car1, car1], (entry2, p2): [car2, car1, car2, car2]},
            exit2: {(entry3, p1): [car2, car1, car3, car3],
                    (entry3, p2): [car3, car3, car3, car1, car2]}}

        res = a.compute_function_per_exit(stats)

        self.assertEqual({exit1: {entry1: 10, entry2: 20}, exit2: {entry3: 30}}, res[3])

    def test_should_compute_median_for_exit_nodes(self):
        s = Simulator()
        entry1 = Entry(s, 0, 1)
        entry2 = Entry(s, 0, 1)
        entry3 = Entry(s, 0, 1)

        p1 = Path([])
        p2 = Path([])

        exit1 = Exit(s, 1)
        exit2 = Exit(s, 1)

        a = Analytics({}, [])

        road1 = Road(s, 100, Orientation.SOUTH, 1)

        car1 = Car(p2, entry1, 0)
        car2 = Car(p2, entry2, 0)
        car3 = Car(p2, entry3, 0)

        nodes = []

        for i in range(0, 10):
            nodes.append(road1.nodes[0][i])

        car1.visited_nodes = nodes

        nodes1 = []

        for i in range(0, 20):
            nodes1.append(road1.nodes[0][i])

        car2.visited_nodes = nodes1

        nodes2 = []

        for i in range(0, 30):
            nodes2.append(road1.nodes[0][i])

        car3.visited_nodes = nodes2

        stats = {
            exit1: {(entry1, p1): [car1, car1, car1, car1, car1], (entry2, p2): [car1, car1, car2, car2]},
            exit2: {(entry3, p1): [car2, car1, car3, car3],
                    (entry3, p2): [car3, car3, car3, car1, car2]}}

        res = a.compute_function_per_exit(stats)

        self.assertEqual({exit1: {entry1: 10, entry2: 15}, exit2: {entry3: 30}}, res[1])

    def test_should_compute_the_stop_time_for_each_arrived_cars(self):
        s = Simulator()
        entry1 = Entry(s, 0, 1)
        entry2 = Entry(s, 0, 1)
        entry3 = Entry(s, 0, 1)

        p1 = Path([])
        p2 = Path([])

        exit1 = Exit(s, 1)
        exit2 = Exit(s, 1)

        road1 = Road(s, 100, Orientation.SOUTH, 1)

        car1 = Car(p2, entry1, 0)
        car2 = Car(p2, entry2, 0)
        car3 = Car(p2, entry3, 0)
        car4 = Car(p2, entry1, 0)
        car5 = Car(p2, entry2, 0)
        car6 = Car(p2, entry3, 0)

        nodes = []

        for i in range(0, 10):
            nodes.append(road1.nodes[0][i])

        car1.visited_nodes = nodes
        car6.visited_nodes = nodes
        nodes1 = []

        for i in range(0, 20):
            nodes1.append(road1.nodes[0][i])

        car2.visited_nodes = nodes1
        car4.visited_nodes = nodes1
        nodes2 = []

        for i in range(0, 30):
            nodes2.append(road1.nodes[0][i])

        car3.visited_nodes = nodes2
        car5.visited_nodes = nodes2

        car1.original_path.nodes = nodes
        car2.original_path.nodes = nodes
        car3.original_path.nodes = nodes
        car4.original_path.nodes = nodes
        car5.original_path.nodes = nodes
        car6.original_path.nodes = nodes

        stats = {exit1: {(entry1, p1): [car1, car2, car3, car6]},
                 exit2: {(entry2, p1): [car4, car5]}}

        a = Analytics([], [])

        res = a.compute_delay_time_by_car(stats)

        self.assertFalse(car1 in res)
        self.assertTrue(car2 in res)
        self.assertTrue(car3 in res)
        self.assertTrue(car4 in res)
        self.assertTrue(car5 in res)
        self.assertFalse(car6 in res)

        self.assertEqual(10, res[car2])
        self.assertEqual(20, res[car3])
        self.assertEqual(10, res[car4])
        self.assertEqual(20, res[car5])

    def test_should_compute_the_delay_time_expectancy_with_traffic_load(self):
        s = Simulator()
        entry1 = Entry(s, 0, 1)
        entry2 = Entry(s, 0, 1)
        entry3 = Entry(s, 0, 1)

        p1 = Path([])
        p2 = Path([])

        exit1 = Exit(s, 1)
        exit2 = Exit(s, 1)

        road1 = Road(s, 100, Orientation.SOUTH, 1)

        car1 = Car(p2, entry1, 0)
        car2 = Car(p2, entry2, 0)
        car3 = Car(p2, entry3, 0)
        car4 = Car(p2, entry1, 0)
        car5 = Car(p2, entry2, 0)
        car6 = Car(p2, entry3, 0)

        nodes = []

        for i in range(0, 10):
            nodes.append(road1.nodes[0][i])

        car1.visited_nodes = nodes
        car6.visited_nodes = nodes
        nodes1 = []

        for i in range(0, 20):
            nodes1.append(road1.nodes[0][i])

        car2.visited_nodes = nodes1
        car4.visited_nodes = nodes1
        nodes2 = []

        for i in range(0, 30):
            nodes2.append(road1.nodes[0][i])

        car3.visited_nodes = nodes2
        car5.visited_nodes = nodes2

        car1.original_path.nodes = nodes
        car2.original_path.nodes = nodes
        car3.original_path.nodes = nodes
        car4.original_path.nodes = nodes
        car5.original_path.nodes = nodes
        car6.original_path.nodes = nodes

        car1.departure_tick = 1
        car2.departure_tick = 1
        car3.departure_tick = 2
        car4.departure_tick = 3
        car5.departure_tick = 3
        car6.departure_tick = 4

        stats = {exit1: {(entry1, p1): [car1, car2, car3, car6]},
                 exit2: {(entry2, p1): [car4, car5]}}

        t_load = []

        for i in range(0, 50):
            t_load.append(0)

        t_load[1] = 2
        t_load[2] = 3
        t_load[3] = 5
        t_load[4] = 6

        for i in range(5, 11):
            t_load[i] = 6

        for i in range(11, 15):
            t_load[i] = 5

        for i in range(15, 21):
            t_load[i] = 4

        for i in range(21, 24):
            t_load[i] = 3

        for i in range(24, 32):
            t_load[i] = 2

        t_load[32] = 1
        t_load[33] = 1

        a = Analytics([], t_load)

        delay = a.compute_delay_time_by_car(stats)

        res = a.compute_delay_time_expectancy_with_traffic_load(delay)

        self.assertEqual(100, res[1])
        self.assertEqual(250, res[2])
        self.assertEqual(250, res[8])
        self.assertAlmostEqual(300, res[22], delta=0.1)
        self.assertEqual(400, res[28])


if __name__ == '__main__':
    unittest.main()
