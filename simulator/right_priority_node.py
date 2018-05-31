from simulator.traffic_node import TrafficNode


class RightPriorityNode(TrafficNode):
    def __init__(self):
        TrafficNode.__init__(self)
        self.priorityMap = {}

    def can_move(self, node):
        if node in self.priorityMap:
            return not (self.is_car_present or self.priorityMap.get(node).is_car_present)
        else:
            return not self.is_car_present

    # first node has to let the priority to the second
    def add_priority(self, node1, node2):
        self.priorityMap[node1] = node2

    def __str__(self):
        return "+"
