from simulator import AbstractEntity, Node, link


class RightPriorityJunction(AbstractEntity):

    def __init__(self, simulator, n_of_entry, n_of_exit):
        super().__init__(simulator)
        self.nodes = [Node()]
        self.n_of_entry = n_of_entry
        self.n_of_exit = n_of_exit

    def do_add_predecessor(self, orientation, predecessor):
        end = predecessor.get_end(orientation)
        start = self.get_start(orientation)
        link(end, start)
        self.simulator.dependencies[(end, start)] = [start]
        if orientation.left() in self.predecessors:
            super().simulator.dependencies[(end, start)].append(orientation.left())

    def compute_next(self):
        for n in self.nodes:
            n.compute_next(self.simulator)

    def apply_next(self):
        for n in self.nodes:
            n.apply_next()

    def get_start(self, orientation):
        return self.nodes[0]

    def get_end(self, orientation):
        return self.nodes[0]
