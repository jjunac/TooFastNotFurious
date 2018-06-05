from simulator import link, AbstractEntity

class Road(AbstractEntity):

    def __init__(self, simulator,  length, orientation, n_of_ways):
        super().__init__(simulator)
        self.nodes = [build_road(length, orientation) for _ in range(n_of_ways)]
        self.length = length
        self.n_of_ways = n_of_ways
        self.orientation = orientation
        self.__link_ways()

    def __link_ways(self):
        # TODO link dependencies when we decide multiple ways
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
        super().simulator.dependencies[(end, start)] = [start]

    def __build_road(simulator, length, orientation):
        res = [RoadNode(orientation)]
        for i in range(length - 1):
            res.append(RoadNode(orientation))
            link(res[-2], res[-1])
        return res
