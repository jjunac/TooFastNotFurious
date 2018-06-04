from simulator import Statistics
from simulator.traffic_node import TrafficNode


class ExitNode(TrafficNode):

    def __init__(self):
        super().__init__()
        self.outflow = 0
        self.departure_counter = {}
        self.statistics = Statistics()

    def can_move(self, node):
        return True

    def compute_next(self):
        super().compute_next()
        if self.current_car:
            departure = self.current_car.departure
            if not departure in self.departure_counter:
                self.departure_counter[departure] = 0
            self.departure_counter[departure] += 1
            self.outflow += 1
            self.statistics.add_travel_time(departure, self.current_car.tick)

    def compute_average_time(self):
        average = []
        for departure in self.departure_counter:
            av = self.statistics.compute_average(departure, self.departure_counter[departure])
            average.append((departure, av))
        return average
