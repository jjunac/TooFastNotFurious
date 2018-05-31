from simulator.traffic_node import TrafficNode


class ExitNode(TrafficNode):

    def __init__(self):
        super().__init__()
        self.outflow = 0

    def can_move(self, node):
        return True

    def compute_next(self):
        super().compute_next()
        if self.current_car:
            self.outflow += 1
