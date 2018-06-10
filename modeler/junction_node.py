from modeler.node import Node
import simulator
from modeler.road import Road
from shared import Orientation


class JunctionNode(Node):

    def __init__(self):
        super().__init__()

    def get_io_roads(self):
        io_roads = {
            Orientation.NORTH: (
                self.entries[Orientation.SOUTH].n_ways if Orientation.SOUTH in self.entries else 0,
                self.exits[Orientation.NORTH].n_ways if Orientation.NORTH in self.exits else 0
            ),
            Orientation.EAST: (
                self.entries[Orientation.WEST].n_ways if Orientation.WEST in self.entries else 0,
                self.exits[Orientation.EAST].n_ways if Orientation.EAST in self.exits else 0
            ),
            Orientation.SOUTH: (
                self.entries[Orientation.NORTH].n_ways if Orientation.NORTH in self.entries else 0,
                self.exits[Orientation.SOUTH].n_ways if Orientation.SOUTH in self.exits else 0
            ),
            Orientation.WEST: (
                self.entries[Orientation.EAST].n_ways if Orientation.EAST in self.entries else 0,
                self.exits[Orientation.WEST].n_ways if Orientation.WEST in self.exits else 0
            )
        }
        return io_roads
