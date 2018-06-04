class Statistics:

    def __init__(self):
        self.list_time_travel = {}

    def add_travel_time(self, path, time):
        if not path in self.list_time_travel:
            self.list_time_travel[path] = []
        self.list_time_travel[path].append(time)
