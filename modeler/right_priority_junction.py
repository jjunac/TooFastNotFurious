from modeler.junction_node import JunctionNode
from modeler.node import Node
import simulator
from modeler.road import Road
from shared import Orientation


class RightPriorityJunction(JunctionNode):

    def __init__(self):
        super().__init__()

    def build(self, sim):
        return simulator.RightPriorityJunction(sim, self.get_io_roads())
