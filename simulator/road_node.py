from simulator.traffic_node import TrafficNode


class RoadNode(TrafficNode):

    def __init__(self, orientation):
        super().__init__()
        self.orientation = orientation

    def can_move(self, node):
        return self.current_car is None

    def __str__(self):
        return "_"
