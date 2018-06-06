class Statistics:

    def __init__(self):
        self.list_time_travel = {}

    def add_travel_time(self, departure, path, time):
        if not (departure, path) in self.list_time_travel:
            self.list_time_travel[(departure, path)] = []
        self.list_time_travel[(departure, path)].append(time)
