from abc import ABC, abstractmethod


class TrafficNode(ABC):
    def __init__(self):
        self.successors = []
        self.predecessors = []
        self.is_car_present = False
        self.next_is_car_present = False

    @abstractmethod
    def can_move(self, node):
        pass

    def compute_next(self):
        # FIXME always send to the first successor
        if self.is_car_present and self.successors[0].can_move(self):
            self.next_is_car_present = False
            self.successors[0].next_is_car_present = True

    def apply_next(self):
        self.is_car_present = self.next_is_car_present
