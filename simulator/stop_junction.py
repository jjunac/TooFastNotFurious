from shared import Orientation
from simulator.right_priority_junction import RightPriorityJunction
from simulator.node import Node
from simulator.utils import link


class StopJunction(RightPriorityJunction):

    def __init__(self, simulator, io_roads):
        super().__init__(simulator, io_roads)

    def do_add_predecessor(self, orientation, predecessor):
        end = predecessor.get_end(orientation.invert())
        start = self.get_start(orientation.invert())
        for i in range(len(start)):
            link(end[i], start[i])
            self.simulator.dependencies[(end[i], start[i])] = [start[i]]
        # This car needs to leave the priority to the car on the left (so heading right)
        if orientation.right() in self.predecessors and self.io_roads[orientation][2] == True:
            end_of_predecessor = self.get_end_of_predecessor(orientation.right())
            for i in range(len(end_of_predecessor)):
                self.simulator.dependencies[(end_of_predecessor[i], self.get_start(orientation.right())[i])].extend(end)
        # This car needs to leave the priority to the car on the right (so heading left)
        if orientation.left() in self.predecessors and self.io_roads[orientation][2] == True:
            end_of_predecessor = self.get_end_of_predecessor(orientation.left())
            print(end_of_predecessor)
            for i in range(len(end_of_predecessor)):
                self.simulator.dependencies[(end_of_predecessor[i], self.get_start(orientation.left())[i])].extend(end)
