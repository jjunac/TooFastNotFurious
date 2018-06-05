from simulator.exit import Exit
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

    def get_stats(self):
        stats = {}
        exit_nodes = [n for n in self.entities if type(n) is Exit]
        for node in exit_nodes:
            stats[node] = node.get_stats()

        return stats
