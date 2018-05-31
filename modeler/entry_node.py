from modeler.node import Node
import simulator

class EntryNode(Node):

    def __init__(self):
        super().__init__()

    def build(self):
        return simulator.EntryNode(0.5)