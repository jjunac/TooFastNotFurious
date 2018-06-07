from collections import deque


class Path:

    def __init__(self, nodes):
        self.nodes = deque(nodes)


    def next_node(self):
        return self.nodes[0]


    def pop_node(self):
        return self.nodes.popleft()
