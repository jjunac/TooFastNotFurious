from modeler.node import Node
import simulator
from modeler.road import Road
from shared import Orientation


class RightPriorityJunction(Node):

    def __init__(self):
        super().__init__()

    def build(self, sim):
        io_roads = {}
        i_north = 1
        o_south = 1
        o_west = 1
        i_east = 1
        if Orientation.NORTH in self.entries:
            i_north = self.entries[Orientation.NORTH].n_ways
        if Orientation.SOUTH in self.exits:
            o_south = self.exits[Orientation.SOUTH].n_ways
        if Orientation.EAST in self.entries:
            i_east = self.entries[Orientation.EAST].n_ways
        if Orientation.WEST in self.exits:
            o_west = self.exits[Orientation.WEST].n_ways
        io_roads[Orientation.NORTH] = (i_north, o_south)
        io_roads[Orientation.EAST] = (i_east, o_west)
        return simulator.RightPriorityJunction(sim, io_roads)
