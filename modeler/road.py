import simulator

class Road:

    def __init__(self, start, orientation_start):
        self.length = 0
        self.start = start
        self.end = None
        self.orientation_start = orientation_start
        self.orientation_end = orientation_start.invert()

    def with_length(self, length):
        self.length = length
        return self

    def to(self, destination):
        self.end = destination
        destination.entries[self.orientation_end] = self
        return self

    def build(self):
        self.start.possible_destinations[self.end] = (len(self.start.possible_destinations.items()), self.length)
        return simulator.Road(self.length, self.orientation_start, 1)