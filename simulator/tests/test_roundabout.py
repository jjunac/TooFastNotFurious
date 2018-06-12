import unittest

from shared import Orientation
from simulator import Simulator, Road
from simulator.roundabout import Roundabout


class TestRoundabout(unittest.TestCase):

    def test_roundabout_internal_mesh_should_be_well_connected(self):
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

        round.add_predecessor(Orientation.NORTH, in_N)
        round.add_predecessor(Orientation.EAST, in_E)
        round.add_predecessor(Orientation.SOUTH, in_S)
        round.add_predecessor(Orientation.WEST, in_W)
        out_S.add_predecessor(Orientation.SOUTH, round)
        out_W.add_predecessor(Orientation.WEST, round)
        out_N.add_predecessor(Orientation.NORTH, round)
        out_E.add_predecessor(Orientation.EAST, round)

        # self.assertEqual({out_S.nodes[0][0], round.yields[Orientation.NORTH].nodes[0][1]}, set(round.yields[Orientation.NORTH].nodes[0][0].successors))

        