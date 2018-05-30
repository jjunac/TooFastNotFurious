from engine.traffic_node import TrafficNode


class RoadNode(TrafficNode):
    def __init__(self):
        super().__init__()

    def can_move(self, node):
        return not self.is_car_present
