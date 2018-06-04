from simulator import build_road, link, AbstractEntity

class Road(AbstractEntity):

    def __init__(self, length, orientation, n_of_ways):
        self.ways = [build_road(length, orientation) for _ in range(n_of_ways)]
        self.length = length
        self.n_of_ways = n_of_ways
        self.orientation = orientation
        self.nodes = build_road(length, orientation)

    def link_ways(self):
        for i in range(self.n_of_ways):
            if i == 0:
                for j in range(self.length - 1):
                    link(self.ways[i][j], self.ways[i + 1][j + 1])
            elif i == self.n_of_ways - 1:
                for j in range(self.length - 1):
                    link(self.ways[i][j], self.ways[i - 1][j + 1])
            else:
                for j in range(self.length - 1):
                    link(self.ways[i][j], self.ways[i + 1][j + 1])
                    link(self.ways[i][j], self.ways[i - 1][j + 1])
