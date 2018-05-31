import random

from simulator.car import Car
from simulator.traffic_node import TrafficNode
from copy import deepcopy


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
        if self.to_spawn > 0 and self.successors[0].current_car is None:
            probas = sorted(self.paths.keys())
            draw = random.random()
            for p in probas:
                if draw <= p/100:
                    self.next_car = Car(deepcopy(self.paths[p]))
                    self.to_spawn -= 1
                    break
