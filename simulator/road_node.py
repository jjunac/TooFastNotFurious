from simulator.abstract_node import AbstractNode


class RoadNode(AbstractNode):

    def __init__(self, orientation):
        super().__init__()
        self.orientation = orientation

    def can_move(self, node):
        return self.current_car is None
