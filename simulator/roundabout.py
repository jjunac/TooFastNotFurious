from abc import ABC
from simulator import StopJunction
from simulator.abstract_entity import AbstractEntity


class Roundabout(AbstractEntity, ABC):

    def __init__(self, simulator, io_roads, n_of_ways):
        self.io_roads = io_roads
        self.n_of_ways = n_of_ways
        self.entities = []
        self.yields = {}
        for o in io_roads.keys():
            ios = {}
            ios[o] = io_roads[o]
            ios[o.invert()] = io_roads[o]
            ios[o.left()] = (n_of_ways, 0)
            ios[o.right()] = (0, n_of_ways)
            self.yields[o] = StopJunction(simulator, ios, o)
        super().__init__(simulator, self.get_nodes())

    def do_add_predecessor(self, orientation, predecessor):
        self.yields[orientation].add_predecessor(orientation, predecessor)

    def get_end_of_predecessor(self, orientation):
        return self.predecessors[orientation].get_end(orientation)

    def compute_next(self):
        for row in self.nodes:
            for n in row:
                n.compute_next(self.simulator)

    def apply_next(self):
        for row in self.nodes:
            for n in row:
                n.apply_next()

    def get_start(self, orientation):
        self.yields[orientation].get_start(orientation)

    def get_end(self, orientation):
        self.yields[orientation].get_end(orientation)

    def is_dependency_satisfied(self, source):
        return True
