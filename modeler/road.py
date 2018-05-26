class Road:

    def __init__(self):
        self.length = 0
        self.start = None
        self.end = None

    # TODO metaprograming to avoid repetition ?
    def with_length(self, length):
        self.length = length
        return self

    def that_starts(self, start):
        self.start = start
        return self

    def that_ends(self, end):
        self.end = end
        return self