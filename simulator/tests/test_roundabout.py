import unittest

from shared import Orientation, dijkstra_with_path
from simulator import Simulator, Road, Car, Path
from simulator.roundabout import Roundabout


class TestRoundabout(unittest.TestCase):

    def test_roundabout_internal_mesh_should_be_well_connected(self):
        simulator = Simulator()
        round = Roundabout(simulator, {Orientation.NORTH: (1, 1), Orientation.EAST: (1, 1),
                                      Orientation.SOUTH: (1, 1), Orientation.WEST: (1, 1)}, 1)

        self.assertEqual({round.yields[Orientation.NORTH].nodes[0][0]}, set(round.yields[Orientation.NORTH].nodes[0][1].successors))
        self.assertEqual({round.roads[Orientation.NORTH].nodes[0][0]}, set(round.yields[Orientation.NORTH].nodes[0][0].successors))
        self.assertEqual({round.roads[Orientation.NORTH].nodes[0][1]}, set(round.roads[Orientation.NORTH].nodes[0][0].successors))
        self.assertEqual({round.yields[Orientation.WEST].nodes[1][0]}, set(round.roads[Orientation.NORTH].nodes[0][1].successors))

        self.assertEqual({round.yields[Orientation.WEST].nodes[0][0]}, set(round.yields[Orientation.WEST].nodes[1][0].successors))
        self.assertEqual({round.roads[Orientation.WEST].nodes[0][0]}, set(round.yields[Orientation.WEST].nodes[0][0].successors))
        self.assertEqual({round.roads[Orientation.WEST].nodes[0][1]}, set(round.roads[Orientation.WEST].nodes[0][0].successors))
        self.assertEqual({round.yields[Orientation.SOUTH].nodes[0][0]}, set(round.roads[Orientation.WEST].nodes[0][1].successors))

        self.assertEqual({round.yields[Orientation.SOUTH].nodes[0][1]}, set(round.yields[Orientation.SOUTH].nodes[0][0].successors))
        self.assertEqual({round.roads[Orientation.SOUTH].nodes[0][0]}, set(round.yields[Orientation.SOUTH].nodes[0][1].successors))
        self.assertEqual({round.roads[Orientation.SOUTH].nodes[0][1]}, set(round.roads[Orientation.SOUTH].nodes[0][0].successors))
        self.assertEqual({round.yields[Orientation.EAST].nodes[0][0]}, set(round.roads[Orientation.SOUTH].nodes[0][1].successors))

        self.assertEqual({round.yields[Orientation.EAST].nodes[1][0]}, set(round.yields[Orientation.EAST].nodes[0][0].successors))
        self.assertEqual({round.roads[Orientation.EAST].nodes[0][0]}, set(round.yields[Orientation.EAST].nodes[1][0].successors))
        self.assertEqual({round.roads[Orientation.EAST].nodes[0][1]}, set(round.roads[Orientation.EAST].nodes[0][0].successors))
        self.assertEqual({round.yields[Orientation.NORTH].nodes[0][1]}, set(round.roads[Orientation.EAST].nodes[0][1].successors))

    def test_a_roundabout_should_be_well_connected_with_in_out_roads(self):
        simulator = Simulator()
        round = Roundabout(simulator, {Orientation.NORTH: (1, 1), Orientation.EAST: (1, 1),
                                      Orientation.SOUTH: (1, 1), Orientation.WEST: (1, 1)}, 1)
        in_N = Road(simulator, 1, Orientation.NORTH, 1)
        in_E = Road(simulator, 1, Orientation.EAST, 1)
        in_S = Road(simulator, 1, Orientation.SOUTH, 1)
        in_W = Road(simulator, 1, Orientation.WEST, 1)
        out_S = Road(simulator, 1, Orientation.SOUTH, 1)
        out_W = Road(simulator, 1, Orientation.WEST, 1)
        out_N = Road(simulator, 1, Orientation.NORTH, 1)
        out_E = Road(simulator, 1, Orientation.NORTH, 1)

        round.add_predecessor(Orientation.NORTH, in_N)
        round.add_predecessor(Orientation.EAST, in_E)
        round.add_predecessor(Orientation.SOUTH, in_S)
        round.add_predecessor(Orientation.WEST, in_W)
        out_S.add_predecessor(Orientation.SOUTH, round)
        out_W.add_predecessor(Orientation.WEST, round)
        out_N.add_predecessor(Orientation.NORTH, round)
        out_E.add_predecessor(Orientation.EAST, round)

        self.assertEqual({round.yields[Orientation.SOUTH].nodes[0][1]}, set(in_N.nodes[0][0].successors))
        self.assertEqual({round.yields[Orientation.SOUTH].nodes[0][0]}, set(out_S.nodes[0][0].predecessors))

        self.assertEqual({round.yields[Orientation.WEST].nodes[0][0]}, set(in_E.nodes[0][0].successors))
        self.assertEqual({round.yields[Orientation.WEST].nodes[1][0]}, set(out_W.nodes[0][0].predecessors))

        self.assertEqual({round.yields[Orientation.NORTH].nodes[0][0]}, set(in_S.nodes[0][0].successors))
        self.assertEqual({round.yields[Orientation.NORTH].nodes[0][1]}, set(out_N.nodes[0][0].predecessors))

        self.assertEqual({round.yields[Orientation.EAST].nodes[1][0]}, set(in_W.nodes[0][0].successors))
        self.assertEqual({round.yields[Orientation.EAST].nodes[0][0]}, set(out_E.nodes[0][0].predecessors))

    def test_a_car_in_the_roundabout_should_have_priority_when_it_is_in_a_roundabout(self):
        simulator = Simulator()
        round = Roundabout(simulator, {Orientation.NORTH: (1, 1), Orientation.EAST: (1, 1),
                                      Orientation.SOUTH: (1, 1), Orientation.WEST: (1, 1)}, 1)
        in_N = Road(simulator, 1, Orientation.NORTH, 1)
        in_E = Road(simulator, 1, Orientation.EAST, 1)
        in_S = Road(simulator, 1, Orientation.SOUTH, 1)
        in_W = Road(simulator, 1, Orientation.WEST, 1)
        out_S = Road(simulator, 1, Orientation.SOUTH, 1)
        out_W = Road(simulator, 1, Orientation.WEST, 1)
        out_N = Road(simulator, 1, Orientation.NORTH, 1)
        out_E = Road(simulator, 1, Orientation.NORTH, 1)

        round.add_predecessor(Orientation.NORTH, in_N)
        round.add_predecessor(Orientation.EAST, in_E)
        round.add_predecessor(Orientation.SOUTH, in_S)
        round.add_predecessor(Orientation.WEST, in_W)
        out_S.add_predecessor(Orientation.SOUTH, round)
        out_W.add_predecessor(Orientation.WEST, round)
        out_N.add_predecessor(Orientation.NORTH, round)
        out_E.add_predecessor(Orientation.EAST, round)

        in_N.nodes[0][0].current_car = Car(Path(dijkstra_with_path(simulator.get_nodes(), simulator.weights, in_N.nodes[0][0], out_S.nodes[0][0])), in_N.nodes[0][0], 0)

        simulator.tick()
        self.assertIsNotNone(round.yields[Orientation.SOUTH].nodes[0][1].current_car)
        simulator.tick()
        self.assertIsNotNone(round.roads[Orientation.SOUTH].nodes[0][0].current_car)
        simulator.tick()
        self.assertIsNotNone(round.roads[Orientation.SOUTH].nodes[0][1].current_car)

        simulator.tick()
        self.assertIsNotNone(round.yields[Orientation.EAST].nodes[0][0].current_car)
        in_W.nodes[0][0].current_car = Car(Path(dijkstra_with_path(simulator.get_nodes(), simulator.weights, in_W.nodes[0][0], out_S.nodes[0][0])), in_W.nodes[0][0], 0)
        simulator.tick()
        self.assertIsNotNone(round.yields[Orientation.EAST].nodes[1][0].current_car)
        self.assertIsNotNone(in_W.nodes[0][0].current_car)
        simulator.tick()
        self.assertIsNotNone(round.roads[Orientation.EAST].nodes[0][0].current_car)
        self.assertIsNotNone(in_W.nodes[0][0].current_car)
        in_W.nodes[0][0].current_car = None
        simulator.tick()
        self.assertIsNotNone(round.roads[Orientation.EAST].nodes[0][1].current_car)

        simulator.tick()
        self.assertIsNotNone(round.yields[Orientation.NORTH].nodes[0][1].current_car)
        in_S.nodes[0][0].current_car = Car(Path(dijkstra_with_path(simulator.get_nodes(), simulator.weights, in_S.nodes[0][0], out_E.nodes[0][0])), in_S.nodes[0][0], 0)
        simulator.tick()
        self.assertIsNotNone(round.yields[Orientation.NORTH].nodes[0][0].current_car)
        self.assertIsNotNone(in_S.nodes[0][0].current_car)
        simulator.tick()
        self.assertIsNotNone(round.roads[Orientation.NORTH].nodes[0][0].current_car)
        self.assertIsNotNone(in_S.nodes[0][0].current_car)
        in_S.nodes[0][0].current_car = None
        simulator.tick()
        self.assertIsNotNone(round.roads[Orientation.NORTH].nodes[0][1].current_car)

        simulator.tick()
        self.assertIsNotNone(round.yields[Orientation.WEST].nodes[1][0].current_car)
        in_E.nodes[0][0].current_car = Car(Path(dijkstra_with_path(simulator.get_nodes(), simulator.weights, in_E.nodes[0][0], out_S.nodes[0][0])), in_E.nodes[0][0], 0)
        simulator.tick()
        self.assertIsNotNone(round.yields[Orientation.WEST].nodes[0][0].current_car)
        self.assertIsNotNone(in_E.nodes[0][0].current_car)
        simulator.tick()
        self.assertIsNotNone(round.roads[Orientation.WEST].nodes[0][0].current_car)
        self.assertIsNotNone(in_E.nodes[0][0].current_car)
        in_E.nodes[0][0].current_car = None
        simulator.tick()
        self.assertIsNotNone(round.roads[Orientation.WEST].nodes[0][1].current_car)
        
        simulator.tick()
        self.assertIsNotNone(round.yields[Orientation.SOUTH].nodes[0][0].current_car)
        in_N.nodes[0][0].current_car = Car(Path(dijkstra_with_path(simulator.get_nodes(), simulator.weights, in_N.nodes[0][0], out_W.nodes[0][0])), in_N.nodes[0][0], 0)
        simulator.tick()
        self.assertIsNotNone(out_S.nodes[0][0].current_car)
        self.assertIsNotNone(in_N.nodes[0][0].current_car)
        simulator.tick()
        self.assertIsNone(out_S.nodes[0][0].current_car)
        self.assertIsNone(in_N.nodes[0][0].current_car)







