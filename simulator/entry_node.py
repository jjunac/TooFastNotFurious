import random

from simulator.Car import Car
from simulator.traffic_node import TrafficNode


class EntryNode(TrafficNode):

    def __init__(self, avg_car_per_tick):
        super().__init__()
        self.avg_car_per_tick = avg_car_per_tick
        self.to_spawn = 0

    def can_move(self, node):
        return False

    def compute_next(self):
        super().compute_next()
        if random.random() <= 0.2:
            self.to_spawn += 1
        if self.to_spawn > 0 and self.successors[0].current_car is None:
            self.next_car = Car()
            self.to_spawn -= 1
