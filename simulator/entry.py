import random

from simulator.node import Node
from simulator.abstract_entity import AbstractEntity
from simulator.car import Car


class Entry(AbstractEntity):

    def __init__(self, simulator, rate, n_of_ways):
        super().__init__(simulator, [[Node(self)] for _ in range(n_of_ways)])
        self.n_of_ways = n_of_ways
        self.rate = rate
        self.paths = {}
        self.to_spawn = [0 for _ in range(n_of_ways)]

    def do_add_predecessor(self, orientation, predecessor):
        RuntimeError("Entry cannot have predecessor")

    def get_start(self, orientation):
        return [row[0] for row in self.nodes]

    def get_end(self, orientation):
        return [row[0] for row in self.nodes]

    def apply_next(self):
        for row in self.nodes:
            for n in row:
                n.apply_next()

    def compute_next(self):
        for row in self.nodes:
            for n in row:
                n.compute_next(self.simulator)
        if random.random() <= self.rate:
            self.to_spawn[random.choice(range(self.n_of_ways))] += 1
        for i in range(self.n_of_ways):
            if self.to_spawn[i] > 0 and not self.nodes[i][0].current_car:
                probas = sorted(self.paths.keys())
                draw = random.random()
                for p in probas:
                    if draw <= p / 100:
                        path = [tmp for tmp in self.paths[p] if tmp.nodes[0] in self.nodes[i][0].successors][0]
                        self.nodes[i][0].next_car = Car(path, self)
                        self.to_spawn[i] -= 1
                        break

    def is_dependency_satisfied(self):
        return True

