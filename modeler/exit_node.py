import engine
from modeler.node import Node


class ExitNode(Node):
    def __init__(self):
        super().__init__()

    def build(self):
        return engine.ExitNode()