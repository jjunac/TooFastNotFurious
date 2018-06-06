from collections import deque


class Path:

    def __init__(self, nodes):
        self.nodes = nodes


    def next_node(self):
        return self.nodes[-1]


    def pop_node(self):
        return self.nodes.pop()
