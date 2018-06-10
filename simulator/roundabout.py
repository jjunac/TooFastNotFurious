from abc import ABC, abstractmethod
from shared import Orientation
from simulator.abstract_entity import AbstractEntity
from simulator.node import Node
from simulator.utils import link


class Roundabout(AbstractEntity, ABC):

    def __init__(self, simulator, io_roads, n_of_ways):
        self.io_roads = io_roads
        self.n_of_ways = n_of_ways
        self.n_ways_N = io_roads[Orientation.NORTH][0] + io_roads[Orientation.NORTH][1]
        self.n_ways_S = io_roads[Orientation.SOUTH][0] + io_roads[Orientation.SOUTH][1]
        self.n_ways_E = io_roads[Orientation.EAST][0] + io_roads[Orientation.EAST][1]
        self.n_ways_W = io_roads[Orientation.WEST][0] + io_roads[Orientation.WEST][1]
        super().__init__(simulator, self.__build_roundabout())
        self.__link_nodes()

    def __build_roundabout(self):
        interval = 2
        length = sum([i for t in self.io_roads.values() for i in t])
        return [[Node(self) for i in range(length + 4 * interval)] for _ in range(self.n_of_ways)]

    def __link_nodes(self):
        # Link a way
        for row in self.nodes:
            for i in range(len(row)):
                link(row[i-1], row[i])
                self.simulator.dependencies[(row[i-1], row[i])] = [row[i]]
        # Link ways
        if self.n_of_ways < 2:
            return
        for i in range(self.n_of_ways):
            if i == 0:
                for j in range(len(self.nodes[i]) - 1):
                    link(self.nodes[i][j], self.nodes[i + 1][j + 1])
                    self.simulator.dependencies[(self.nodes[i][j], self.nodes[i + 1][j + 1])] = \
                        [self.nodes[i + 1][j + 1], self.nodes[i + 1][j]]
            elif i == self.n_of_ways - 1:
                for j in range(len(self.nodes[i]) - 1):
                    link(self.nodes[i][j], self.nodes[i - 1][j + 1])
                    self.simulator.dependencies[(self.nodes[i][j], self.nodes[i - 1][j + 1])] = \
                        [self.nodes[i - 1][j + 1], self.nodes[i - 1][j]]
            else:
                for j in range(len(self.nodes[i]) - 1):
                    link(self.nodes[i][j], self.nodes[i + 1][j + 1])
                    self.simulator.dependencies[(self.nodes[i][j], self.nodes[i + 1][j + 1])] = \
                        [self.nodes[i + 1][j + 1], self.nodes[i + 1][j]]
                    link(self.nodes[i][j], self.nodes[i - 1][j + 1])
                    self.simulator.dependencies[(self.nodes[i][j], self.nodes[i - 1][j + 1])] = \
                        [self.nodes[i + 1][j + 1], self.nodes[i - 1][j]]

    def do_add_predecessor(self, orientation, predecessor):
        end = predecessor.get_end(orientation.invert())
        start = self.get_start(orientation.invert())
        for i in range(len(start)):
            link(end[i], start[i])
            self.simulator.dependencies[(end[i], start[i])] = self.get_nodes()

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
        in_S = self.io_roads[Orientation.SOUTH][0]
        for y in range(len(self.nodes) - 1):
            for x in range(1, in_S + 1):
                link(self.nodes[y][-x], self.nodes[y + 1][-x])
                self.simulator.dependencies[(self.nodes[y][-x], self.nodes[y + 1][-x])] = [self.nodes[y + 1][-x]]
        # from W to E
        in_W = self.io_roads[Orientation.WEST][0]
        for y in range(in_W):
            for x in range(len(self.nodes[y]) - 1):
                link(self.nodes[y][x], self.nodes[y][x + 1])
                self.simulator.dependencies[(self.nodes[y][x], self.nodes[y][x + 1])] = [self.nodes[y][x + 1]]
        # from N to S
        in_N = self.io_roads[Orientation.NORTH][0]
        for y in range(1, len(self.nodes)):
            for x in range(in_N):
                link(self.nodes[y][x], self.nodes[y - 1][x])
                self.simulator.dependencies[(self.nodes[y][x], self.nodes[y - 1][x])] = [self.nodes[y - 1][x]]
        # from E to W
        in_E = self.io_roads[Orientation.EAST][0]
        for y in range(1, in_E + 1):
            for x in range(1, len(self.nodes[-y])):
                link(self.nodes[-y][x], self.nodes[-y][x - 1])
                self.simulator.dependencies[(self.nodes[-y][x], self.nodes[-y][x - 1])] = [self.nodes[-y][x - 1]]

    @abstractmethod
    def is_dependency_satisfied(self, source):
        pass
