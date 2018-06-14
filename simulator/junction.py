from abc import ABC, abstractmethod
from shared import Orientation
from simulator.abstract_entity import AbstractEntity
from simulator.node import Node
from simulator.utils import link


class Junction(AbstractEntity, ABC):

    def __init__(self, simulator, io_roads):
        self.io_roads = io_roads

        n_ways_n = io_roads[Orientation.NORTH][0] + io_roads[Orientation.NORTH][1]
        n_ways_s = io_roads[Orientation.SOUTH][0] + io_roads[Orientation.SOUTH][1]
        n_ways_e = io_roads[Orientation.EAST][0] + io_roads[Orientation.EAST][1]
        n_ways_w = io_roads[Orientation.WEST][0] + io_roads[Orientation.WEST][1]
        if (n_ways_n != n_ways_s and n_ways_n != 0 and n_ways_s != 0) or (n_ways_e != n_ways_w and n_ways_e != 0 and n_ways_w != 0):
                raise RuntimeError("in/out of North/South and East/West must be coherent")

        self.size_north_south = max(n_ways_n, n_ways_s)
        self.size_east_west = max(n_ways_e, n_ways_w)
        super().__init__(simulator, [[Node(self) for i in range(self.size_north_south)] for j in range(self.size_east_west)])
        self.__link_nodes()

    def do_add_predecessor(self, orientation, predecessor):
        end = predecessor.get_end(orientation.invert())
        start = self.get_start(orientation.invert())
        for i in range(len(start)):
            link(end[i], start[i])
            self.simulator.dependencies[(end[i], start[i])] = [start[i]]
            self.simulator.weights[(end[i], start[i])] = 2

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
        in_ways = self.io_roads[orientation][0]
        if orientation == Orientation.NORTH:
            return self.nodes[-1][:in_ways]
        if orientation == Orientation.SOUTH:
            return self.nodes[0][-in_ways:]
        if orientation == Orientation.EAST:
            return [row[-1] for row in self.nodes[-in_ways:]]
        if orientation == Orientation.WEST:
            return [row[0] for row in self.nodes[:in_ways]]

    def get_end(self, orientation):
        out_ways = self.io_roads[orientation][1]
        if orientation == Orientation.NORTH:
            return self.nodes[-1][-out_ways:]
        if orientation == Orientation.SOUTH:
            return self.nodes[0][:out_ways]
        if orientation == Orientation.EAST:
            return [row[-1] for row in self.nodes[:out_ways]]
        if orientation == Orientation.WEST:
            return [row[0] for row in self.nodes[-out_ways:]]

    def __link_nodes(self):
        # from S to N
        in_s = self.io_roads[Orientation.SOUTH][0]
        for y in range(len(self.nodes) - 1):
            for x in range(1, in_s + 1):
                link(self.nodes[y][-x], self.nodes[y + 1][-x])
                self.simulator.dependencies[(self.nodes[y][-x], self.nodes[y + 1][-x])] = [self.nodes[y + 1][-x]]
                self.simulator.weights[(self.nodes[y][-x], self.nodes[y + 1][-x])] = 2
        # from W to E
        in_w = self.io_roads[Orientation.WEST][0]
        for y in range(in_w):
            for x in range(len(self.nodes[y]) - 1):
                link(self.nodes[y][x], self.nodes[y][x + 1])
                self.simulator.dependencies[(self.nodes[y][x], self.nodes[y][x + 1])] = [self.nodes[y][x + 1]]
                self.simulator.weights[(self.nodes[y][x], self.nodes[y][x + 1])] = 2
        # from N to S
        in_n = self.io_roads[Orientation.NORTH][0]
        for y in range(1, len(self.nodes)):
            for x in range(in_n):
                link(self.nodes[y][x], self.nodes[y - 1][x])
                self.simulator.dependencies[(self.nodes[y][x], self.nodes[y - 1][x])] = [self.nodes[y - 1][x]]
                self.simulator.weights[(self.nodes[y][x], self.nodes[y - 1][x])] = 2
        # from E to W
        in_e = self.io_roads[Orientation.EAST][0]
        for y in range(1, in_e + 1):
            for x in range(1, len(self.nodes[-y])):
                link(self.nodes[-y][x], self.nodes[-y][x - 1])
                self.simulator.dependencies[(self.nodes[-y][x], self.nodes[-y][x - 1])] = [self.nodes[-y][x - 1]]
                self.simulator.weights[(self.nodes[-y][x], self.nodes[-y][x - 1])] = 2

    @abstractmethod
    def is_dependency_satisfied(self, source):
        pass
