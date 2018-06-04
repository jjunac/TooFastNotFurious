from simulator import ExitNode
from simulator.utils import *
from visualizer.drawer import Drawing


class Simulator:

    def __init__(self, nodes):
        self.nodes = nodes

    def tick(self):
        compute_next(self.nodes)
        apply_next(self.nodes)
        # print("[%s]" % "".join([str(n) for n in self.nodes]))

    def run(self, ticks):
        for _ in range(ticks):
            self.tick()

    def run_graphical(self, ticks):
        drawing = Drawing(self)
        drawing.draw()

    def compute_average_time(self):
        exit_nodes = [n for n in self.nodes if type(n) is ExitNode]
        for node in exit_nodes:
            node.compute_average_time()
