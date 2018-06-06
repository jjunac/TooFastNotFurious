from copy import deepcopy


class Car:

    def __init__(self, path, departure):
        self.path = deepcopy(path)
        self.original_path = path
        self.departure = departure
        self.time = 0
        self.visited_nodes = []

    def get_way_index(self):
        return self.path.next_direction()

    def go_forward(self):
        self.path.pop_direction()

    def tick(self, node):
        # TODO remove time and use len on the visited_nodes
        self.visited_nodes.append(node)
        self.time += 1
