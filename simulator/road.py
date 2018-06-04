from simulator import build_road, link


class Road:

    def __init__(self, length, orientation, n_of_ways):
        self.ways = []
        for i in range(n_of_ways):
            self.ways.append(build_road(length, orientation))

    def link_ways(self):
        for i in range(len(self.ways)):
            if i == 0:
                for j in range(len(self.ways[i]) - 1):
                    link(self.ways[i][j], self.ways[i + 1][j + 1])
            elif i == len(self.ways) - 1:
                for j in range(len(self.ways[i]) - 1):
                    link(self.ways[i][j], self.ways[i - 1][j + 1])
            else:
                for j in range(len(self.ways[i]) - 1):
                    link(self.ways[i][j], self.ways[i + 1][j + 1])
                    link(self.ways[i][j], self.ways[i - 1][j + 1])
