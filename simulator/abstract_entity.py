from abc import ABC, abstractmethod


class AbstractEntity(ABC):

    def __init__(self, simulator):
        self.simulator = simulator
        self.predecessors = {}
        self.successors = {}

    def add_predecessor(self, orientation, predecessor):
        self.predecessors[orientation] = predecessor
        self.do_add_predecessor(orientation, predecessor)

    @abstractmethod
    def do_add_predecessor(self, orientation, predecessor):
        pass

    def add_successor(self, orientation, successor):
        self.successors[orientation] = successor
        self.do_add_successor(orientation, successor)

    @abstractmethod
    def do_add_successor(self, orientation, successor):
        pass

    @abstractmethod
    def get_start(self, orientation):
        pass

    @abstractmethod
    def get_end(self, orientation):
        pass