import unittest

from shared import Orientation
from simulator import Simulator, Road
from simulator.roundabout import Roundabout


class TestRoundabout(unittest.TestCase):

    def test_a_roundabout_should_be_well_connected(self):
        simulator = Simulator()
        round = Roundabout(simulator, {Orientation.NORTH: (1, 1), Orientation.EAST: (1, 1),
                                      Orientation.SOUTH: (1, 1), Orientation.WEST: (1, 1)}, 2)
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

        