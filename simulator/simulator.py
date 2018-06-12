from simulator.exit import Exit
from statistics.analytics import Analytics
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

    def generate_report(self):
        analytics = Analytics(self.entities)
        analytics.generate_report()

    def get_nodes(self):
        return [n for e in self.entities for n in e.get_nodes()]
