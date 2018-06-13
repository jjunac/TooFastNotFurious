import unittest

from shared import *
from simulator import Simulator, TrafficLightJunction, Road, Car, Path


class TestTrafficLight (unittest.TestCase):

    def test_a_car_should_not_go_when_it_has_a_red_light_and_go_when_it_is_green(self):
        simulator = Simulator()

        tl = TrafficLightJunction(simulator, {Orientation.NORTH: (0, 1), Orientation.EAST: (1, 0), Orientation.SOUTH: (1, 0), Orientation.WEST: (0, 1)},
                                  [Orientation.EAST], 2, [Orientation.SOUTH], 2, 1)
        r1 = Road(simulator, 1, Orientation.NORTH, 1)
        r2 = Road(simulator, 1, Orientation.WEST, 1)
        r3 = Road(simulator, 1, Orientation.WEST, 1)

        r1.nodes[0][0].current_car = Car(Path([tl.nodes[0][0], r3.nodes[0][0]]), r1.nodes[0][0], 0)

        tl.add_predecessor(Orientation.NORTH, r1)
        tl.add_predecessor(Orientation.WEST, r2)
        r3.add_predecessor(Orientation.WEST, tl)

        simulator.tick()
        # Red for 1t
        self.assertEqual(1, tl.counter)
        self.assertIsNotNone(r1.nodes[0][0].current_car)
        self.assertIsNone(r2.nodes[0][0].current_car)
        self.assertIsNone(tl.nodes[0][0].current_car)
        self.assertIsNone(r3.nodes[0][0].current_car)

        simulator.tick()
        # Interval for 1t
        self.assertEqual(2, tl.counter)
        self.assertIsNotNone(r1.nodes[0][0].current_car)
        self.assertIsNone(r2.nodes[0][0].current_car)
        self.assertIsNone(tl.nodes[0][0].current_car)
        self.assertIsNone(r3.nodes[0][0].current_car)

        simulator.tick()
        # Green for 2t
        self.assertEqual(3, tl.counter)
        self.assertIsNotNone(r1.nodes[0][0].current_car)
        self.assertIsNone(r2.nodes[0][0].current_car)
        self.assertIsNone(tl.nodes[0][0].current_car)
        self.assertIsNone(r3.nodes[0][0].current_car)

        simulator.tick()
        # Green for 1t
        self.assertEqual(4, tl.counter)
        self.assertIsNone(r1.nodes[0][0].current_car)
        self.assertIsNone(r2.nodes[0][0].current_car)
        self.assertIsNotNone(tl.nodes[0][0].current_car)
        self.assertIsNone(r3.nodes[0][0].current_car)

    def test_cars_should_respect_traffic_lights_when_there_are_multiple_roads_with_opposite_ways(self):
        simulator = Simulator()
        tl = TrafficLightJunction(simulator, {Orientation.NORTH: (1, 1), Orientation.EAST: (1, 1), Orientation.SOUTH: (1, 1), Orientation.WEST: (1, 1)},
                                  [Orientation.EAST, Orientation.WEST], 5, [Orientation.NORTH, Orientation.SOUTH], 5, 1)
        in_N = Road(simulator, 1, Orientation.NORTH, 1)
        in_E = Road(simulator, 1, Orientation.EAST, 1)
        in_S = Road(simulator, 1, Orientation.SOUTH, 1)
        in_W = Road(simulator, 1, Orientation.WEST, 1)
        out_S = Road(simulator, 1, Orientation.SOUTH, 1)
        out_W = Road(simulator, 1, Orientation.WEST, 1)
        out_N = Road(simulator, 1, Orientation.NORTH, 1)
        out_E = Road(simulator, 1, Orientation.EAST, 1)

        tl.add_predecessor(Orientation.NORTH, in_N)
        tl.add_predecessor(Orientation.EAST, in_E)
        tl.add_predecessor(Orientation.SOUTH, in_S)
        tl.add_predecessor(Orientation.WEST, in_W)
        out_S.add_predecessor(Orientation.SOUTH, tl)
        out_W.add_predecessor(Orientation.WEST, tl)
        out_N.add_predecessor(Orientation.NORTH, tl)
        out_E.add_predecessor(Orientation.EAST, tl)

        in_N.nodes[0][0].current_car = Car(
            Path(dijkstra_with_path(simulator.get_nodes(), simulator.weights, in_N.nodes[0][0], out_W.nodes[0][0])), in_N.nodes[0][0], 0)
        in_E.nodes[0][0].current_car = Car(
            Path(dijkstra_with_path(simulator.get_nodes(), simulator.weights, in_E.nodes[0][0], out_N.nodes[0][0])), in_E.nodes[0][0], 0)
        in_S.nodes[0][0].current_car = Car(
            Path(dijkstra_with_path(simulator.get_nodes(), simulator.weights, in_S.nodes[0][0], out_E.nodes[0][0])), in_S.nodes[0][0], 0)
        in_W.nodes[0][0].current_car = Car(
            Path(dijkstra_with_path(simulator.get_nodes(), simulator.weights, in_W.nodes[0][0], out_S.nodes[0][0])), in_W.nodes[0][0], 0)

        self.assertIsNotNone(in_N.nodes[0][0].current_car)
        self.assertIsNotNone(in_E.nodes[0][0].current_car)
        self.assertIsNotNone(in_S.nodes[0][0].current_car)
        self.assertIsNotNone(in_W.nodes[0][0].current_car)
        self.assertIsNone(tl.nodes[0][0].current_car)
        self.assertIsNone(tl.nodes[0][1].current_car)
        self.assertIsNone(tl.nodes[1][0].current_car)
        self.assertIsNone(tl.nodes[1][1].current_car)
        self.assertIsNone(out_S.nodes[0][0].current_car)
        self.assertIsNone(out_W.nodes[0][0].current_car)
        self.assertIsNone(out_N.nodes[0][0].current_car)
        self.assertIsNone(out_E.nodes[0][0].current_car)

        simulator.tick()
        # EAST/WEST for 4t
        self.assertEqual(1, tl.counter)
        self.assertIsNotNone(in_N.nodes[0][0].current_car)
        self.assertIsNone(in_E.nodes[0][0].current_car)
        self.assertIsNotNone(in_S.nodes[0][0].current_car)
        self.assertIsNone(in_W.nodes[0][0].current_car)
        self.assertIsNotNone(tl.nodes[0][0].current_car)
        self.assertIsNone(tl.nodes[0][1].current_car)
        self.assertIsNone(tl.nodes[1][0].current_car)
        self.assertIsNotNone(tl.nodes[1][1].current_car)
        self.assertIsNone(out_S.nodes[0][0].current_car)
        self.assertIsNone(out_W.nodes[0][0].current_car)
        self.assertIsNone(out_N.nodes[0][0].current_car)
        self.assertIsNone(out_E.nodes[0][0].current_car)

        simulator.tick()
        # EAST/WEST for 3t
        self.assertEqual(2, tl.counter)
        self.assertIsNotNone(in_N.nodes[0][0].current_car)
        self.assertIsNone(in_E.nodes[0][0].current_car)
        self.assertIsNotNone(in_S.nodes[0][0].current_car)
        self.assertIsNone(in_W.nodes[0][0].current_car)
        self.assertIsNone(tl.nodes[0][0].current_car)
        self.assertIsNotNone(tl.nodes[0][1].current_car)
        self.assertIsNotNone(tl.nodes[1][0].current_car)
        self.assertIsNone(tl.nodes[1][1].current_car)
        self.assertIsNone(out_S.nodes[0][0].current_car)
        self.assertIsNone(out_W.nodes[0][0].current_car)
        self.assertIsNone(out_N.nodes[0][0].current_car)
        self.assertIsNone(out_E.nodes[0][0].current_car)

        simulator.tick()
        # EAST/WEST for 2t
        self.assertEqual(3, tl.counter)
        self.assertIsNotNone(in_N.nodes[0][0].current_car)
        self.assertIsNone(in_E.nodes[0][0].current_car)
        self.assertIsNotNone(in_S.nodes[0][0].current_car)
        self.assertIsNone(in_W.nodes[0][0].current_car)
        self.assertIsNotNone(tl.nodes[0][0].current_car)
        self.assertIsNone(tl.nodes[0][1].current_car)
        self.assertIsNone(tl.nodes[1][0].current_car)
        self.assertIsNotNone(tl.nodes[1][1].current_car)
        self.assertIsNone(out_S.nodes[0][0].current_car)
        self.assertIsNone(out_W.nodes[0][0].current_car)
        self.assertIsNone(out_N.nodes[0][0].current_car)
        self.assertIsNone(out_E.nodes[0][0].current_car)

        simulator.tick()
        # EAST/WEST for 1t
        self.assertEqual(4, tl.counter)
        self.assertIsNotNone(in_N.nodes[0][0].current_car)
        self.assertIsNone(in_E.nodes[0][0].current_car)
        self.assertIsNotNone(in_S.nodes[0][0].current_car)
        self.assertIsNone(in_W.nodes[0][0].current_car)
        self.assertIsNone(tl.nodes[0][0].current_car)
        self.assertIsNone(tl.nodes[0][1].current_car)
        self.assertIsNone(tl.nodes[1][0].current_car)
        self.assertIsNone(tl.nodes[1][1].current_car)
        self.assertIsNotNone(out_S.nodes[0][0].current_car)
        self.assertIsNone(out_W.nodes[0][0].current_car)
        self.assertIsNotNone(out_N.nodes[0][0].current_car)
        self.assertIsNone(out_E.nodes[0][0].current_car)

        simulator.tick()
        # Interval for 1t
        self.assertEqual(5, tl.counter)
        self.assertIsNotNone(in_N.nodes[0][0].current_car)
        self.assertIsNone(in_E.nodes[0][0].current_car)
        self.assertIsNotNone(in_S.nodes[0][0].current_car)
        self.assertIsNone(in_W.nodes[0][0].current_car)
        self.assertIsNone(tl.nodes[0][0].current_car)
        self.assertIsNone(tl.nodes[0][1].current_car)
        self.assertIsNone(tl.nodes[1][0].current_car)
        self.assertIsNone(tl.nodes[1][1].current_car)
        self.assertIsNone(out_S.nodes[0][0].current_car)
        self.assertIsNone(out_W.nodes[0][0].current_car)
        self.assertIsNone(out_N.nodes[0][0].current_car)
        self.assertIsNone(out_E.nodes[0][0].current_car)

        simulator.tick()
        # NORTH/SOUTH for 5t
        self.assertEqual(6, tl.counter)
        self.assertIsNotNone(in_N.nodes[0][0].current_car)
        self.assertIsNone(in_E.nodes[0][0].current_car)
        self.assertIsNotNone(in_S.nodes[0][0].current_car)
        self.assertIsNone(in_W.nodes[0][0].current_car)
        self.assertIsNone(tl.nodes[0][0].current_car)
        self.assertIsNone(tl.nodes[0][1].current_car)
        self.assertIsNone(tl.nodes[1][0].current_car)
        self.assertIsNone(tl.nodes[1][1].current_car)
        self.assertIsNone(out_S.nodes[0][0].current_car)
        self.assertIsNone(out_W.nodes[0][0].current_car)
        self.assertIsNone(out_N.nodes[0][0].current_car)
        self.assertIsNone(out_E.nodes[0][0].current_car)

        simulator.tick()
        # NORTH/SOUTH for 4t
        self.assertEqual(7, tl.counter)
        self.assertIsNone(in_N.nodes[0][0].current_car)
        self.assertIsNone(in_E.nodes[0][0].current_car)
        self.assertIsNone(in_S.nodes[0][0].current_car)
        self.assertIsNone(in_W.nodes[0][0].current_car)
        self.assertIsNone(tl.nodes[0][0].current_car)
        self.assertIsNotNone(tl.nodes[0][1].current_car)
        self.assertIsNotNone(tl.nodes[1][0].current_car)
        self.assertIsNone(tl.nodes[1][1].current_car)
        self.assertIsNone(out_S.nodes[0][0].current_car)
        self.assertIsNone(out_W.nodes[0][0].current_car)
        self.assertIsNone(out_N.nodes[0][0].current_car)
        self.assertIsNone(out_E.nodes[0][0].current_car)

        simulator.tick()
        # NORTH/SOUTH for 3t
        self.assertEqual(8, tl.counter)
        self.assertIsNone(in_N.nodes[0][0].current_car)
        self.assertIsNone(in_E.nodes[0][0].current_car)
        self.assertIsNone(in_S.nodes[0][0].current_car)
        self.assertIsNone(in_W.nodes[0][0].current_car)
        self.assertIsNotNone(tl.nodes[0][0].current_car)
        self.assertIsNone(tl.nodes[0][1].current_car)
        self.assertIsNone(tl.nodes[1][0].current_car)
        self.assertIsNotNone(tl.nodes[1][1].current_car)
        self.assertIsNone(out_S.nodes[0][0].current_car)
        self.assertIsNone(out_W.nodes[0][0].current_car)
        self.assertIsNone(out_N.nodes[0][0].current_car)
        self.assertIsNone(out_E.nodes[0][0].current_car)

        simulator.tick()
        # NORTH/SOUTH for 2t
        self.assertEqual(9, tl.counter)
        self.assertIsNone(in_N.nodes[0][0].current_car)
        self.assertIsNone(in_E.nodes[0][0].current_car)
        self.assertIsNone(in_S.nodes[0][0].current_car)
        self.assertIsNone(in_W.nodes[0][0].current_car)
        self.assertIsNone(tl.nodes[0][0].current_car)
        self.assertIsNotNone(tl.nodes[0][1].current_car)
        self.assertIsNotNone(tl.nodes[1][0].current_car)
        self.assertIsNone(tl.nodes[1][1].current_car)
        self.assertIsNone(out_S.nodes[0][0].current_car)
        self.assertIsNone(out_W.nodes[0][0].current_car)
        self.assertIsNone(out_N.nodes[0][0].current_car)
        self.assertIsNone(out_E.nodes[0][0].current_car)

        simulator.tick()
        # NORTH/SOUTH for 1t
        self.assertEqual(10, tl.counter)
        self.assertIsNone(in_N.nodes[0][0].current_car)
        self.assertIsNone(in_E.nodes[0][0].current_car)
        self.assertIsNone(in_S.nodes[0][0].current_car)
        self.assertIsNone(in_W.nodes[0][0].current_car)
        self.assertIsNone(tl.nodes[0][0].current_car)
        self.assertIsNone(tl.nodes[0][1].current_car)
        self.assertIsNone(tl.nodes[1][0].current_car)
        self.assertIsNone(tl.nodes[1][1].current_car)
        self.assertIsNone(out_S.nodes[0][0].current_car)
        self.assertIsNotNone(out_W.nodes[0][0].current_car)
        self.assertIsNone(out_N.nodes[0][0].current_car)
        self.assertIsNotNone(out_E.nodes[0][0].current_car)

    def test_a_car_should_go_when_it_is_engaged_and_the_light_is_red(self):
        simulator = Simulator()

        tl = TrafficLightJunction(simulator,
                                  {Orientation.NORTH: (0, 1), Orientation.EAST: (1, 0), Orientation.SOUTH: (1, 0),
                                   Orientation.WEST: (0, 1)},
                                  [Orientation.SOUTH], 1, [Orientation.EAST], 1, 3)
        r1 = Road(simulator, 1, Orientation.NORTH, 1)
        r2 = Road(simulator, 1, Orientation.WEST, 1)
        r3 = Road(simulator, 1, Orientation.WEST, 1)

        r1.nodes[0][0].current_car = Car(Path([tl.nodes[0][0], r3.nodes[0][0]]), r1.nodes[0][0], 0)

        tl.add_predecessor(Orientation.NORTH, r1)
        tl.add_predecessor(Orientation.WEST, r2)
        r3.add_predecessor(Orientation.WEST, tl)

        simulator.tick()
        self.assertEqual(1, tl.counter)
        self.assertIsNone(r1.nodes[0][0].current_car)
        self.assertIsNone(r2.nodes[0][0].current_car)
        self.assertIsNotNone(tl.nodes[0][0].current_car)
        self.assertIsNone(r3.nodes[0][0].current_car)

        simulator.tick()
        self.assertEqual(2, tl.counter)
        self.assertIsNone(r1.nodes[0][0].current_car)
        self.assertIsNone(r2.nodes[0][0].current_car)
        self.assertIsNone(tl.nodes[0][0].current_car)
        self.assertIsNotNone(r3.nodes[0][0].current_car)

    def test_a_car_should_move_forward_when_light_goes_from_red_to_green(self):
        simulator = Simulator()

        tl = TrafficLightJunction(simulator,
                                  {Orientation.NORTH: (0, 1), Orientation.EAST: (1, 0), Orientation.SOUTH: (1, 0),
                                   Orientation.WEST: (0, 1)},
                                  [Orientation.SOUTH], 1, [Orientation.EAST], 1, 2)
        r1 = Road(simulator, 1, Orientation.NORTH, 1)
        r2 = Road(simulator, 1, Orientation.WEST, 1)
        r3 = Road(simulator, 1, Orientation.WEST, 1)

        r2.nodes[0][0].current_car = Car(Path([tl.nodes[0][0], r3.nodes[0][0]]), r1.nodes[0][0], 0)

        tl.add_predecessor(Orientation.NORTH, r1)
        tl.add_predecessor(Orientation.WEST, r2)
        r3.add_predecessor(Orientation.WEST, tl)

        # Red for 2t
        simulator.tick()
        self.assertEqual(1, tl.counter)
        self.assertIsNone(r1.nodes[0][0].current_car)
        self.assertIsNotNone(r2.nodes[0][0].current_car)
        self.assertIsNone(tl.nodes[0][0].current_car)
        self.assertIsNone(r3.nodes[0][0].current_car)

        # Red for 1t
        simulator.tick()
        self.assertEqual(2, tl.counter)
        self.assertIsNone(r1.nodes[0][0].current_car)
        self.assertIsNotNone(r2.nodes[0][0].current_car)
        self.assertIsNone(tl.nodes[0][0].current_car)
        self.assertIsNone(r3.nodes[0][0].current_car)

        # Green
        simulator.tick()
        self.assertEqual(3, tl.counter)
        self.assertIsNone(r1.nodes[0][0].current_car)
        self.assertIsNotNone(r2.nodes[0][0].current_car)
        self.assertIsNone(tl.nodes[0][0].current_car)
        self.assertIsNone(r3.nodes[0][0].current_car)

        # Green
        simulator.tick()
        self.assertEqual(4, tl.counter)
        self.assertIsNone(r1.nodes[0][0].current_car)
        self.assertIsNone(r2.nodes[0][0].current_car)
        self.assertIsNotNone(tl.nodes[0][0].current_car)
        self.assertIsNone(r3.nodes[0][0].current_car)

    def test_a_traffic_light_should_restart_after_a_full_rotation(self):
        simulator = Simulator()

        tl = TrafficLightJunction(simulator,
                                  {Orientation.NORTH: (0, 1), Orientation.EAST: (1, 0), Orientation.SOUTH: (1, 0),
                                   Orientation.WEST: (0, 1)},
                                  [Orientation.SOUTH], 1, [Orientation.EAST], 1, 1)
        self.assertEqual(0, tl.counter)
        simulator.tick()
        self.assertEqual(1, tl.counter)
        simulator.tick()
        self.assertEqual(2, tl.counter)
        simulator.tick()
        self.assertEqual(3, tl.counter)
        simulator.tick()
        self.assertEqual(0, tl.counter)
        simulator.tick()
        self.assertEqual(1, tl.counter)
        simulator.tick()
        self.assertEqual(2, tl.counter)
        simulator.tick()
        self.assertEqual(3, tl.counter)

