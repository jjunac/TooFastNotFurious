from abc import ABC, abstractmethod

from simulator.traffic_node import TrafficNode


class RightPriorityNode(TrafficNode):
    def __init__(self):
        TrafficNode.__init__(self)
        self.priorityMap = {}

    def can_move(self, node):
        if node in self.priorityMap:
            return self.current_car is None and self.priorityMap.get(node).current_car is None
            #return not (self.is_car_present or self.priorityMap.get(node).is_car_present)
        else:
            return self.current_car is None

    # first node has to let the priority to the second
    def add_priority(self, node1, node2):
        self.priorityMap[node1] = node2
