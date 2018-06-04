from simulator.utils import *
from visualizer.drawer import Drawing


class Simulator:

    def __init__(self, nodes):
        self.nodes = nodes
        self.dependencies = {}

    def tick(self):
        compute_next(self.nodes)
        apply_next(self.nodes)

    def run(self, ticks):
        for _ in range(ticks):
            self.tick()

    def run_graphical(self, ticks):
        drawing = Drawing(self)
        drawing.draw()
