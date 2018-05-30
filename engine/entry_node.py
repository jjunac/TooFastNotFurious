from engine.state import State
from engine.entity import Entity
import random


class EntryNode(Entity):

    def __init__(self, avg_car_per_tick, road):
        self.to_spawn = 0
        self.avg_car_per_tick = avg_car_per_tick
        self.road = road

    def tick(self):
        if random.random() >= 0.5:
            self.to_spawn += 1
        if self.to_spawn > 0 and self.road.get_state(0) == State.EMPTY:
            self.road.set_state(0, State.CAR)
            self.to_spawn -= 1
