from engine.utils import *

class Simulation:
    def __init__(self, nodes):
        self.nodes = nodes

    def tick(self):
        compute_next(self.nodes)
        apply_next(self.nodes)

        