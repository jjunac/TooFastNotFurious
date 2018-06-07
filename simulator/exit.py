from simulator.statistics import Statistics
from simulator.abstract_entity import AbstractEntity
from simulator.utils import link
from simulator.node import Node


class Exit(AbstractEntity):

    def __init__(self, simulator, n_of_ways):
        super().__init__(simulator, [[Node()] for _ in range(n_of_ways)])
        self.n_of_ways = n_of_ways
        self.outflow = 0
        self.departure_counter = {}
        self.statistics = Statistics()

    def compute_next(self):
        for row in self.nodes:
            for n in row:
                if n.current_car:
                    departure = n.current_car.departure
                    if not departure in self.departure_counter:
                        self.departure_counter[departure] = 0
                    self.departure_counter[departure] += 1
                    self.outflow += 1
                    self.statistics.add_travel_time(n.current_car.departure, n.current_car.original_path,
                                                    n.current_car.time)

    def do_add_predecessor(self, orientation, predecessor):
        end = predecessor.get_end(orientation.invert())
        start = self.get_start(orientation.invert())
        for i in range(self.n_of_ways):
            link(end[i], start[i])
            self.simulator.dependencies[(end[i], start[i])] = [start[i]]

    def get_start(self, orientation):
        return [row[0] for row in self.nodes]

    def get_end(self, orientation):
        return [row[0] for row in self.nodes]

    def apply_next(self):
        for row in self.nodes:
            for n in row:
                n.apply_next()

    def get_stats(self):
        return self.statistics.list_time_travel
