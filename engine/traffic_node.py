from abc import ABC, abstractmethod


class TrafficNode(ABC):
    def __init__(self):
        self.successors = []
        self.predecessors = []
        self.is_car_present = False

    @abstractmethod
    def can_move(self, node):
        pass
