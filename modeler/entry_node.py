from modeler.path import Path
from modeler.node import Node
import simulator

class EntryNode(Node):

    def __init__(self):
        super().__init__()
        self.rate = 0


    def with_rate(self, rate):
        self.rate = rate
        return self


    def go_through(self, *junctions):
        p = Path(self)
        p.junctions = junctions
        return p


    def build(self):
        return simulator.EntryNode(0.5, self.rate)