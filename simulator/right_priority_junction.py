from shared import Orientation
from simulator.abstract_entity import AbstractEntity
from simulator.node import Node
from simulator.utils import link


class RightPriorityJunction(AbstractEntity):

    def __init__(self, simulator, io_roads):
        self.io_roads = io_roads
        n_ways_N = io_roads[Orientation.NORTH][0] + io_roads[Orientation.NORTH][1]
        n_ways_S = io_roads[Orientation.SOUTH][0] + io_roads[Orientation.SOUTH][1]
        n_ways_E = io_roads[Orientation.EAST][0] + io_roads[Orientation.EAST][1]
        n_ways_W = io_roads[Orientation.WEST][0] + io_roads[Orientation.WEST][1]
        if (n_ways_N != n_ways_S and n_ways_N != 0 and n_ways_S != 0) or (n_ways_E != n_ways_W and n_ways_E != 0 and n_ways_W != 0):
                raise RuntimeError("in/out of North/South and East/West must be coherent")
        self.size_north_south = max(n_ways_N, n_ways_S)
        self.size_east_west = max(n_ways_E, n_ways_W)
        super().__init__(simulator, [[Node() for i in range(self.size_north_south)] for j in range(self.size_east_west)])
        self.__link_nodes()

    def do_add_predecessor(self, orientation, predecessor):
        end = predecessor.get_end(orientation.invert())
        start = self.get_start(orientation.invert())
        for i in range(len(start)):
            link(end[i], start[i])
            self.simulator.dependencies[(end[i], start[i])] = self.get_nodes()
        # The car on the left (so heading right) needs to leave the priority
        if orientation.right() in self.predecessors:
            for i in range(len(start)):
                self.simulator.dependencies[(end[i], start[i])].extend(self.get_end_of_predecessor(orientation.right()))
        # This car needs to leave the priority to the car on the right (so heading left)
        if orientation.left() in self.predecessors:
            end_of_predecessor = self.get_end_of_predecessor(orientation.left())
            for i in range(len(end_of_predecessor)):
                self.simulator.dependencies[(end_of_predecessor[i], self.get_start(orientation.left())[i])].extend(end)

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
