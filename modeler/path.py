class Path:

    def __init__(self, departure):
        self.departure = departure
        self.junctions = []
        self.proportion = 0

    def with_proportion(self, percentage):
        self.proportion = percentage
        return self