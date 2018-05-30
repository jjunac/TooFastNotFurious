from engine.state import State
import random

from engine.traffic_node import TrafficNode


class ExitNode(TrafficNode):

    def __init__(self):
        super().__init__()

    def can_move(self, node):
        return True