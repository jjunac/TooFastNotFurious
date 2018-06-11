from simulator.exit import Exit
from statistics.analytics import Analytics
from visualizer.drawer import Drawer


class Simulator:

    def __init__(self):
        self.entities = []
        self.dependencies = {}
        self.traffic_load = []

    def add_entities(self, entity):
        self.entities.append(entity)

    def tick(self):
        for e in self.entities:
            e.compute_next()
        for e in self.entities:
            e.apply_next()

        self.traffic_load.append(
            len([n for n in self.get_nodes() if n.current_car is not None and type(n.entity) is not Exit]))

    def run(self, ticks):
        for _ in range(ticks):
            self.tick()

    def run_graphical(self, ticks):
        drawing = Drawer(self)
        drawing.init_screen()
        drawing.draw()

    def generate_report(self):
        analytics = Analytics(self.entities, self.traffic_load)
        analytics.generate_report()
        analytics.compute_stop_time()

    def get_nodes(self):
        return [n for e in self.entities for n in e.get_nodes()]
