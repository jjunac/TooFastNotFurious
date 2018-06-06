from simulator.statistics import Statistics
from simulator.abstract_entity import AbstractEntity
from simulator.utils import link
from simulator.node import Node


class Exit(AbstractEntity):

    def __init__(self, simulator):
        super().__init__(simulator, [[Node()]])
        self.outflow = 0
        self.departure_counter = {}
        self.statistics = Statistics()

    def compute_next(self):
        for row in self.nodes:
            for n in row:
                if n.current_car:
                    departure = self.nodes[0][0].current_car.departure
                    if not departure in self.departure_counter:
                        self.departure_counter[departure] = 0
                    self.departure_counter[departure] += 1
                    self.outflow += 1
                    self.statistics.add_travel_time(self.nodes[0][0].current_car.departure, self.nodes[0][0].current_car.original_path,
                                                    self.nodes[0][0].current_car.time)

    def do_add_predecessor(self, orientation, predecessor):
        end = predecessor.get_end(orientation)
        start = self.get_start(orientation)
        link(end, start)
        self.simulator.dependencies[(end, start)] = [start]

    def get_start(self, orientation):
        return self.nodes[0][0]

    def get_end(self, orientation):
        return self.nodes[0][0]

    def apply_next(self):
        for row in self.nodes:
            for n in row:
                n.apply_next()

    def get_stats(self):
        return self.statistics.list_time_travel
