from modeler.node import Node
import simulator


class RightPriorityJunction(Node):

    def __init__(self):
        super().__init__()


    def build(self, sim):
        return simulator.RightPriorityJunction(sim, 1, 1)