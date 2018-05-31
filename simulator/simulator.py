from simulator.utils import *

class Simulator:

    def __init__(self, nodes):
        self.nodes = nodes


    def tick(self):
        compute_next(self.nodes)
        apply_next(self.nodes)
        print("[%s]" % "".join([str(n) for n in self.nodes]))

    def run(self, ticks):
        for _ in range(ticks):
            self.tick()
