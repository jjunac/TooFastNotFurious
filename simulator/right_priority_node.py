from simulator.traffic_node import TrafficNode


class RightPriorityNode(TrafficNode):
    def __init__(self):
        TrafficNode.__init__(self)

    def can_move(self, node):
        if not self.current_car:
            priority = self.get_successor_from_orientation(node.orientation.right())
            return not priority or not priority.current_car
        else:
            return False

    def get_successor_from_orientation(self, orientation):
        res = list(filter(lambda s: s.orientation.invert() == orientation, self.predecessors))
        return res[0] if res else None

    def __str__(self):
        return "+"
