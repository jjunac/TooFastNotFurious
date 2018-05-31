import random

from simulator.traffic_node import TrafficNode


class EntryNode(TrafficNode):

    def __init__(self, avg_car_per_tick):
        super().__init__()
        self.avg_car_per_tick = avg_car_per_tick
        self.paths = {}
        self.to_spawn = 0


    def can_move(self, node):
        return False


    def compute_next(self):
        super().compute_next()
        if random.random() <= 0.2:
            self.to_spawn += 1
        if self.to_spawn > 0 and not self.successors[0].is_car_present:
            self.next_is_car_present = True
            self.to_spawn -= 1
