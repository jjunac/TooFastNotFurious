from simulator.statistics import Statistics
from simulator.abstract_entity import AbstractEntity
from simulator.utils import link
from simulator.node import Node


class Exit(AbstractEntity):

    def __init__(self, simulator):
        super().__init__(simulator)
        self.outflow = 0
        self.departure_counter = {}
        self.nodes = [Node()]
        self.statistics = Statistics()

    def compute_next(self):
        if self.nodes[0].current_car:
            departure = self.nodes[0].current_car.departure
            if not departure in self.departure_counter:
                self.departure_counter[departure] = 0
            self.departure_counter[departure] += 1
            self.outflow += 1
            self.statistics.add_travel_time(self.nodes[0].current_car.departure, self.nodes[0].current_car.original_path,
                                            self.nodes[0].current_car.time)

    def do_add_predecessor(self, orientation, predecessor):
        end = predecessor.get_end(orientation)
        link(end, self.nodes[0])
        self.simulator.dependencies[(end, self.nodes[0])] = [self.nodes[0]]

    def get_start(self, orientation):
        return self.nodes[0]

    def get_end(self, orientation):
        return self.nodes[0]

    def apply_next(self):
        self.nodes[0].apply_next()

    def get_stats(self):
        return self.statistics.list_time_travel
