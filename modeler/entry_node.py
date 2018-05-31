from modeler.path import Path
from modeler.node import Node
import simulator

class EntryNode(Node):

    def __init__(self):
        super().__init__()


    def go_through(self, *junctions):
        p = Path(self)
        p.junctions = junctions
        return p


    def build(self):
        return simulator.EntryNode(0.5)