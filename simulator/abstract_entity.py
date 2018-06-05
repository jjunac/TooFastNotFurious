from abc import ABC, abstractmethod


class AbstractEntity(ABC):

    def __init__(self, simulator):
        self.simulator = simulator
        self.predecessors = {}
        self.successors = {}

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
