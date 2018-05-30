from engine.state import State
import random

from engine.traffic_node import TrafficNode


class EntryNode(TrafficNode):

    def __init__(self, avg_car_per_tick):
        super().__init__()
        self.avg_car_per_tick = avg_car_per_tick
        self.to_spawn = 0

    def compute_next(self):
        if random.random() >= 0.5:
            self.to_spawn += 1
        if self.to_spawn > 0 and not self.successors[0].is_car_present:
            self.next_is_car_present = True
            self.to_spawn -= 1
