from modeler.node import Node
import simulator
from modeler.road import Road
from shared import Orientation


class RightPriorityJunction(Node):

    def __init__(self):
        super().__init__()

    def build(self, sim):
        n_way_north = self.exits.get(Orientation.NORTH, Road(None, Orientation.NORTH).with_n_ways(0)).n_ways + \
                      self.entries.get(Orientation.SOUTH, Road(None, Orientation.SOUTH).with_n_ways(0)).n_ways

        n_way_south = self.exits.get(Orientation.SOUTH, Road(None, Orientation.SOUTH).with_n_ways(0)).n_ways + \
                      self.entries.get(Orientation.NORTH, Road(None, Orientation.NORTH).with_n_ways(0)).n_ways

        n_way_east = self.exits.get(Orientation.EAST, Road(None, Orientation.EAST).with_n_ways(0)).n_ways + \
                     self.entries.get(Orientation.WEST, Road(None, Orientation.WEST).with_n_ways(0)).n_ways

        n_way_west = self.exits.get(Orientation.WEST, Road(None, Orientation.WEST).with_n_ways(0)).n_ways + \
                     self.entries.get(Orientation.EAST, Road(None, Orientation.EAST).with_n_ways(0)).n_ways

        size_north_south = max(n_way_north, n_way_south)
        size_east_west = max(n_way_east, n_way_west)

        return simulator.RightPriorityJunction(sim, size_north_south, size_east_west)
