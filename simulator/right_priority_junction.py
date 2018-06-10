from shared import Orientation
from simulator.junction import Junction
from simulator.node import Node
from simulator.utils import link


class RightPriorityJunction(Junction):

    def __init__(self, simulator, io_roads):
        super().__init__(simulator, io_roads)

    def do_add_predecessor(self, orientation, predecessor):
        super().do_add_predecessor(orientation, predecessor)
        end = predecessor.get_end(orientation.invert())
        start = self.get_start(orientation.invert())
        # The car on the left (so heading right) needs to leave the priority
        if orientation.right() in self.predecessors:
            for i in range(len(start)):
                self.simulator.dependencies[(end[i], start[i])].extend(self.get_end_of_predecessor(orientation.right()))
        # This car needs to leave the priority to the car on the right (so heading left)
        if orientation.left() in self.predecessors:
            end_of_predecessor = self.get_end_of_predecessor(orientation.left())
            for i in range(len(end_of_predecessor)):
                self.simulator.dependencies[(end_of_predecessor[i], self.get_start(orientation.left())[i])].extend(end)

    def is_dependency_satisfied(self):
        return True