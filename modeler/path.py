class Path:

    def __init__(self, departure, destination):
        self.departure = departure
        self.destination = destination
        self.proportion = 0

    def with_proportion(self, percentage):
        self.proportion = percentage
        return self