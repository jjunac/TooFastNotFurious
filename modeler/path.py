class Path:

    def __init__(self, destination):
        self.destination = destination
        self.proportion = 0


    def with_proportion(self, percentage):
        self.proportion = percentage