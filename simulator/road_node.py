from simulator.traffic_node import TrafficNode


class RoadNode(TrafficNode):

    def __init__(self, orientation):
        super().__init__()
        self.orientation = orientation

    def can_move(self, node):
        return not self.is_car_present
