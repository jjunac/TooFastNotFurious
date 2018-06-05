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
        drawing.draw()
