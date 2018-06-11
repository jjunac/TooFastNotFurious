from abc import ABC

from shared import Orientation
from simulator import StopJunction, Road
from simulator.abstract_entity import AbstractEntity


class Roundabout(AbstractEntity, ABC):

    INTERVAL = 2

    def __init__(self, simulator, io_roads, n_of_ways):
        self.io_roads = io_roads
        self.n_of_ways = n_of_ways
        self.entities = []
        self.yields = {}
        self.roads = {}
        for o in io_roads.keys():
            ios = {}
            ios[o] = io_roads[o]
            ios[o.invert()] = io_roads[o]
            ios[o.left()] = (n_of_ways, 0)
            ios[o.right()] = (0, n_of_ways)
            stop = StopJunction(simulator, ios, o)
            self.yields[o] = stop
            self.entities.append(stop)
        for o in self.yields.keys():
            road = Road(simulator, self.INTERVAL, o.invert(), n_of_ways)
            road.add_predecessor(o.invert(), self.yields[o])
            self.yields[o.left()].add_predecessor(o, road)
            self.roads[o] = road
            self.entities.append(road)
        super().__init__(simulator, self.get_nodes())

    def do_add_predecessor(self, orientation, predecessor):
        self.yields[orientation.invert()].add_predecessor(orientation, predecessor)

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
        return self.yields[orientation].get_start(orientation)

    def get_end(self, orientation):
        return self.yields[orientation].get_end(orientation)

    def is_dependency_satisfied(self, source):
        return True

    def get_nodes(self):
        nodes = [[] for _ in range(self.n_of_ways)]
        for o in self.yields.keys():
            for i in range(self.n_of_ways):
                nodes[i].extend(self.yields[o].nodes[i])
                nodes[i].extend(self.roads[o].nodes[i])
        return nodes

