from modeler.node import Node
from simulator import RightPriorityNode


class RightPriorityJunction(Node):

    def __init__(self):
        super().__init__()


    def build(self):
        return RightPriorityNode()