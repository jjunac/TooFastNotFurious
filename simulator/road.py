import simulator

class Road:

    def __init__(self, start, orientation_start):
        self.length = 0
        self.number_of_ways = 1
        self.start = start
        self.end = None
        self.orientation_start = orientation_start
        self.orientation_end = orientation_start.invert()