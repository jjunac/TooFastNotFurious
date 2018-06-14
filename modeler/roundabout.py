from modeler.junction_node import JunctionNode
from modeler.node import Node
import simulator
from modeler.road import Road
from shared import Orientation


class Roundabout(JunctionNode):

    def __init__(self):
        super().__init__()
        self.n_ways = 0

    def with_n_ways(self, n_ways):
        self.n_ways = n_ways
        return self

    def build(self, sim):
        return simulator.Roundabout(sim, self.get_io_roads(), self.n_ways)
