from modeler.node import Node
import engine

class EntryNode(Node):

    def __init__(self):
        super().__init__()

    def build(self):
        return engine.EntryNode(0.5)