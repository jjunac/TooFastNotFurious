from simulator.abstract_entity import AbstractEntity
from simulator.node import Node
from simulator.utils import link


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
            self.simulator.dependencies[(end, start)].append(self.get_end_of_predecessor(orientation.left()))
        if orientation.right() in self.predecessors:
            self.simulator.dependencies[(self.get_end_of_predecessor(orientation.right()), start)].append(end)


    def get_end_of_predecessor(self, orientation):
        return self.predecessors[orientation].get_end(orientation)

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
