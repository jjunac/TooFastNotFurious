from abc import ABC, abstractmethod


class AbstractEntity(ABC):

    def __init__(self, simulator, nodes):
        self.simulator = simulator
        self.simulator.add_entities(self)
        self.predecessors = {}
        self.successors = {}
        self.nodes = nodes

    def add_predecessor(self, orientation, predecessor):
        self.predecessors[orientation] = predecessor
        predecessor.successors[orientation] = self
        self.do_add_predecessor(orientation, predecessor)

    @abstractmethod
    def do_add_predecessor(self, orientation, predecessor):
        pass

    @abstractmethod
    def get_start(self, orientation):
        pass

    @abstractmethod
    def get_end(self, orientation):
        pass

    @abstractmethod
    def compute_next(self):
        pass

    @abstractmethod
    def apply_next(self):
        pass
