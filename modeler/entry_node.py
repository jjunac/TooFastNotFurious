from modeler.node import Node
import simulator

class EntryNode(Node):

    def __init__(self):
        super().__init__()
        self.paths = {}


    def add_path(self, path):
        self.paths[path] = path.proportion


    def build(self):

        return simulator.EntryNode(0.5)