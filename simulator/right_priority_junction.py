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
        self.__link_nodes()

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
        in_way = self.io_roads.get(orientation, self.io_roads.get(orientation.invert()))[0]
        if orientation == Orientation.NORTH:
            return self.nodes[0][in_way:]
        if orientation == Orientation.SOUTH:
            return self.nodes[-1][:in_way]
        if orientation == Orientation.EAST:
            return [row[0] for row in self.nodes[in_way:]]
        if orientation == Orientation.WEST:
            return [row[-1] for row in self.nodes[:in_way]]

    def get_end(self, orientation):
        out_way = self.io_roads.get(orientation, self.io_roads.get(orientation.invert()))[1]
        if orientation == Orientation.NORTH:
            return self.nodes[-1][out_way:]
        if orientation == Orientation.SOUTH:
            return self.nodes[0][:out_way]
        if orientation == Orientation.EAST:
            return [row[-1] for row in self.nodes[out_way:]]
        if orientation == Orientation.WEST:
            return [row[0] for row in self.nodes[:out_way]]

    def __link_nodes(self):
        #North entry
        out_NS = self.io_roads[Orientation.NORTH][1]
        for i in range(out_NS, self.size_north_south):
            for j in range(self.size_east_west - 1):
                link(self.nodes[j][i], self.nodes[j+1][i])
        #South exit
        for i in range(out_NS):
            for j in range( self.size_east_west):
                link(self.nodes[j][i], self.nodes[j-1][i])
        #East entry
        for i in range(self.io_roads[Orientation.EAST][0]):
            for j in range(self.size_north_south - 1):
                link(self.nodes[i][j], self.nodes[i][j+1])
        #West exit
        for i in range(self.io_roads[Orientation.EAST][0],self.size_east_west):
            for j in range( self.size_north_south):
                link(self.nodes[i][j], self.nodes[i][j-1])
