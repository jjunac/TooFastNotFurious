from simulator.traffic_node import TrafficNode


class ExitNode(TrafficNode):

    def __init__(self):
        super().__init__()

    def can_move(self, node):
        return True