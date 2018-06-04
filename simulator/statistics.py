class Statistics:

    def __init__(self):
        self.list_time_travel = {}

    def add_travel_time(self, departure, time):
        if not departure in self.list_time_travel:
            self.list_time_travel[departure] = 0
        self.list_time_travel[departure] += time

    def compute_average(self, departure, number_departure):
        return self.list_time_travel[departure] / number_departure
