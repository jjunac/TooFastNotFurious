from simulator.exit import Exit
from visualizer.drawer import Drawer


class Simulator:

    def __init__(self):
        self.entities = []
        self.dependencies = {}

    def add_entities(self, entity):
        self.entities.append(entity)

    def tick(self):
        for e in self.entities:
            e.compute_next()
        for e in self.entities:
            e.apply_next()

    def run(self, ticks):
        for _ in range(ticks):
            self.tick()

    def run_graphical(self, ticks):
        drawing = Drawer(self)
        drawing.init_screen()
        drawing.draw()

    def get_stats(self):
        stats = {}
        exit_nodes = [n for n in self.entities if type(n) is Exit]
        for node in exit_nodes:
            stats[node] = node.get_stats()

        return stats
