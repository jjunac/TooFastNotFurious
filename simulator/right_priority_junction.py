from shared import Orientation
from simulator.abstract_entity import AbstractEntity
from simulator.node import Node
from simulator.utils import link


class RightPriorityJunction(AbstractEntity):

    def __init__(self, simulator, io_roads):
        self.io_roads = io_roads
        self.size_north_south = io_roads[Orientation.NORTH][0] + io_roads[Orientation.NORTH][1]
        self.size_east_west = io_roads[Orientation.EAST][0] + io_roads[Orientation.EAST][1]
        super().__init__(simulator,
                         [[Node() for i in range(self.size_north_south)] for j in range(self.size_east_west)])

    def do_add_predecessor(self, orientation, predecessor):
        end = predecessor.get_end(orientation)
        start = self.get_start(orientation)
        link(end, start)
        self.simulator.dependencies[(end, start)] = [start]
        if orientation.left() in self.predecessors:
            self.simulator.dependencies[(end, start)].append(self.get_end_of_predecessor(orientation.left()))
        if orientation.right() in self.predecessors:
            self.simulator.dependencies[(self.get_end_of_predecessor(orientation.right()), start)].append(end)

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
        if orientation == Orientation.NORTH:
            return self.nodes[0][self.io_roads[orientation][1]:self.size_north_south]
        if orientation == Orientation.SOUTH:
            return self.nodes[-1][0:self.io_roads[orientation][1]-1]
        if orientation == Orientation.EAST:
            res = []
            for i in range(self.io_roads[orientation][0]):
                res.append(self.nodes[0][i])
            return res
        if orientation == Orientation.WEST:
            res = []
            for i in range(self.io_roads[orientation][0],self.size_east_west):
                res.append(self.nodes[-1][i])
            return res

    def get_end(self, orientation):
        if orientation == Orientation.NORTH:
            return self.nodes[-1][self.io_roads[orientation][1]:self.size_north_south]
        if orientation == Orientation.SOUTH:
            return self.nodes[0][0:self.io_roads[orientation][1]-1]
        if orientation == Orientation.EAST:
            res = []
            for i in range(self.io_roads[orientation][0]):
                res.append(self.nodes[-1][i])
            return res
        if orientation == Orientation.WEST:
            res = []
            for i in range(self.io_roads[orientation][0],self.size_east_west):
                res.append(self.nodes[0][i])
            return res

    def __link_nodes(self):
        #North entry
        for i in range(self.io_roads[Orientation.NORTH][1], self.size_north_south):
            for j in range(self.size_east_west - 1):
                link(self.nodes[i][j], self.nodes[i][j+1])
        #South exit
        for i in range(self.io_roads[Orientation.NORTH][1]):
            for j in range(1, self.size_east_west):
                link(self.nodes[i][j], self.nodes[i][j-1])
        #East entry
        for i in range(self.io_roads[Orientation.EAST][1], self.size_east_west):
            for j in range(self.size_north_south - 1):
                link(self.nodes[i][j], self.nodes[i][j+1])
        #West exit
        for i in range(self.io_roads[Orientation.EAST][1]):
            for j in range(1, self.size_north_south):
                link(self.nodes[i][j], self.nodes[i][j-1])
