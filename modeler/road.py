import simulator

class Road:

    def __init__(self, start, orientation):
        self.length = 0
        self.n_ways = 1
        self.start = start
        self.end = None
        self.orientation = orientation

    def with_length(self, length):
        self.length = length
        return self

    def to(self, destination):
        self.end = destination
        destination.entries[self.orientation] = self
        return self

    def with_n_ways(self, n_ways):
        self.n_ways = n_ways
        return self

    def build(self, sim):
        self.start.possible_destinations[self.end] = (len(self.start.possible_destinations.items()), self.length)
        return simulator.Road(sim, self.length, self.orientation, self.n_ways)