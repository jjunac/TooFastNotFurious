import random

from simulator.node import Node
from simulator.abstract_entity import AbstractEntity
from simulator.car import Car


class Entry(AbstractEntity):

    def __init__(self, simulator, rate):
        super().__init__(simulator, [[Node()]])
        self.rate = rate
        self.paths = {}
        self.to_spawn = 0

    def do_add_predecessor(self, orientation, predecessor):
        RuntimeError("Entry cannot have predecessor")

    def get_start(self, orientation):
        return self.nodes[0][0]

    def get_end(self, orientation):
        return self.nodes[0][0]

    def apply_next(self):
        for row in self.nodes:
            for n in row:
                n.apply_next()

    def compute_next(self):
        for row in self.nodes:
            for n in row:
                n.compute_next(self.simulator)
        if random.random() <= self.rate:
            self.to_spawn += 1
        if self.to_spawn > 0 and not self.nodes[0][0].current_car:
            probas = sorted(self.paths.keys())
            draw = random.random()
            for p in probas:
                if draw <= p / 100:
                    self.nodes[0][0].next_car = Car(self.paths[p], self)
                    self.to_spawn -= 1
                    break
