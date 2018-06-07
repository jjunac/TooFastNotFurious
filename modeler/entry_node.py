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


    def to(self, destination):
        p = Path(self, destination)
        return p


    def build(self, sim):
        return simulator.Entry(sim, self.rate, list(self.exits.values())[0].n_ways)