from simulator import AbstractEntity, Node


class Road(AbstractEntity):

    def __init__(self, simulator,  length, orientation, n_of_ways):
        super().__init__(simulator)
        self.nodes = [self.__build_road(simulator, length) for _ in range(n_of_ways)]
        self.length = length
        self.n_of_ways = n_of_ways
        self.orientation = orientation
        self.__link_ways()

    def get_start(self, orientation):
        return self.nodes[0][0]

    def get_end(self, orientation):
        return self.nodes[-1][0]

    def compute_next(self):
        for l in self.nodes:
            for n in l:
                n.compute_next(self.simulator)

    def apply_next(self):
        for l in self.nodes:
            for n in l:
                n.apply_next()

    def __link_ways(self):
        # TODO link dependencies when we decide multiple ways
        if self.n_of_ways < 2:
            return
        for i in range(self.n_of_ways):
            if i == 0:
                for j in range(self.length - 1):
                    link(self.nodes[i][j], self.nodes[i + 1][j + 1])
            elif i == self.n_of_ways - 1:
                for j in range(self.length - 1):
                    link(self.nodes[i][j], self.nodes[i - 1][j + 1])
            else:
                for j in range(self.length - 1):
                    link(self.nodes[i][j], self.nodes[i + 1][j + 1])
                    link(self.nodes[i][j], self.nodes[i - 1][j + 1])

    def do_add_predecessor(self, orientation, predecessor):
        end = predecessor.get_end(orientation)
        start = self.get_start(orientation)
        link(end, start)
        self.simulator.dependencies[(end, start)] = [start]

    def __build_road(self, simulator, length):
        res = [Node()]
        for _ in range(length - 1):
            res.append(Node())
            link(res[-2], res[-1])
            simulator.dependencies[(res[-2], res[-1])] = [res[-1]]
        return res
# FIXME remove and use import
def link(predecessor, successor):
    predecessor.successors.append(successor)
    successor.predecessors.append(predecessor)