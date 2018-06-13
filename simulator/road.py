import math

from simulator.abstract_entity import AbstractEntity
from simulator.node import Node
from simulator.utils import link


class Road(AbstractEntity):

    def __init__(self, simulator,  length, orientation, n_of_ways):
        super().__init__(simulator, [self.__build_road(simulator, length) for _ in range(n_of_ways)])
        self.length = length
        self.n_of_ways = n_of_ways
        self.orientation = orientation
        self.__link_ways()

    def get_start(self, orientation):
        return [row[0] for row in self.nodes]

    def get_end(self, orientation):
        return [row[-1] for row in self.nodes]

    def compute_next(self):
        for l in self.nodes:
            for n in l:
                n.compute_next(self.simulator)

    def apply_next(self):
        for l in self.nodes:
            for n in l:
                n.apply_next()

    def __link_ways(self):
        if self.n_of_ways < 2:
            return
        for i in range(self.n_of_ways):
            if i == 0:
                for j in range(self.length - 1):
                    link(self.nodes[i][j], self.nodes[i + 1][j + 1])
                    self.simulator.dependencies[(self.nodes[i][j], self.nodes[i + 1][j + 1])] = \
                        [self.nodes[i + 1][j + 1], self.nodes[i + 1][j]]
                    self.simulator.weights[(self.nodes[i][j], self.nodes[i + 1][j + 1])] = math.sqrt(2)
            elif i == self.n_of_ways - 1:
                for j in range(self.length - 1):
                    link(self.nodes[i][j], self.nodes[i - 1][j + 1])
                    self.simulator.dependencies[(self.nodes[i][j], self.nodes[i - 1][j + 1])] = \
                        [self.nodes[i - 1][j + 1], self.nodes[i - 1][j]]
                    self.simulator.weights[(self.nodes[i][j], self.nodes[i - 1][j + 1])] = math.sqrt(2)
            else:
                for j in range(self.length - 1):
                    link(self.nodes[i][j], self.nodes[i + 1][j + 1])
                    self.simulator.dependencies[(self.nodes[i][j], self.nodes[i + 1][j + 1])] = \
                        [self.nodes[i + 1][j + 1], self.nodes[i + 1][j]]
                    self.simulator.weights[(self.nodes[i][j], self.nodes[i + 1][j + 1])] = math.sqrt(2)
                    link(self.nodes[i][j], self.nodes[i - 1][j + 1])
                    self.simulator.dependencies[(self.nodes[i][j], self.nodes[i - 1][j + 1])] = \
                        [self.nodes[i + 1][j + 1], self.nodes[i - 1][j]]
                    self.simulator.weights[(self.nodes[i][j], self.nodes[i - 1][j + 1])] = math.sqrt(2)

    def do_add_predecessor(self, orientation, predecessor):
        end = predecessor.get_end(orientation)
        start = self.get_start(orientation)
        for i in range(self.n_of_ways):
            link(end[i], start[i])
            self.simulator.dependencies[(end[i], start[i])] = [start[i]]
            self.simulator.weights[(end[i], start[i])] = 1

    def __build_road(self, simulator, length):
        res = [Node(self, can_ignore_dependency=True)]
        for _ in range(length - 1):
            res.append(Node(self, can_ignore_dependency=True))
            link(res[-2], res[-1])
            simulator.dependencies[(res[-2], res[-1])] = [res[-1]]
            simulator.weights[(res[-2], res[-1])] = 1
        return res

    def is_dependency_satisfied(self, source):
        return True
