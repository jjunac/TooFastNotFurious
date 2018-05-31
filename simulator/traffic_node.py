from abc import ABC, abstractmethod

from simulator.Car import Car


class TrafficNode(ABC):
    def __init__(self):
        self.successors = []
        self.predecessors = []
        self.current_car = None
        self.next_car = None


    @abstractmethod
    def can_move(self, node):
        pass


    def compute_next(self):
        # FIXME always send to the first successor
        if self.current_car is None:
            return
        if len(self.successors) == 0:
            self.next_car = None
            return
        if self.successors[self.current_car.get_way_index()].can_move(self):
            self.successors[self.current_car.get_way_index()].next_car = self.current_car
            self.next_car = None
        else:
            self.next_car = self.current_car


    def apply_next(self):
        self.current_car = self.next_car


    # def __str__(self):
    #     return "#" if self.is_car_present else " "