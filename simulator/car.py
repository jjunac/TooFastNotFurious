from copy import copy

from simulator.path import Path


class Car:

    def __init__(self, path, departure):
        self.path = Path(copy(path.nodes))
        self.original_path = path
        self.departure = departure
        self.time = 0
        self.visited_nodes = []

    def get_next_node(self):
        return self.path.next_node()

    def go_forward(self):
        self.path.pop_node()

    def tick(self, node):
        # TODO remove time and use len on the visited_nodes
        self.visited_nodes.append(node)
        self.time += 1
