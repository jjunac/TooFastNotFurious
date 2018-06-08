from shared import Orientation
from simulator.right_priority_junction import RightPriorityJunction
from simulator.node import Node
from simulator.utils import link


class StopJunction(RightPriorityJunction):

    def __init__(self, simulator, io_roads, orientation_stop):
        self.orientation_stop = orientation_stop
        super().__init__(simulator, io_roads)

    def do_add_predecessor(self, orientation, predecessor):
        # print("coucou", orientation.right())
        # print("coucou", self.predecessors)
        # print("coucou", self.io_roads[orientation.right()])

        end = predecessor.get_end(orientation.invert())
        start = self.get_start(orientation.invert())
        for i in range(len(start)):
            link(end[i], start[i])
            self.simulator.dependencies[(end[i], start[i])] = [start[i]]
        # This car needs to leave the priority to the car on the left (so heading right)

        # print(self.predecessors[Orientation.SOUTH])

        if orientation == self.orientation_stop:
            print("STOP")
            if orientation.right() in self.predecessors:
                for i in range(len(start)):
                    self.simulator.dependencies[(end[i], start[i])].extend(
                        self.get_end_of_predecessor(orientation.right()))

            if orientation.left() in self.predecessors:
                for i in range(len(start)):
                    self.simulator.dependencies[(end[i], start[i])].extend(
                        self.get_end_of_predecessor(orientation.left()))

        else:
            print("ORION", orientation.right(), self.orientation_stop)
            if orientation.right() != self.orientation_stop:
                print("J'AI LA PRIO")
                # The car on the left (so heading right) needs to leave the priority
                if orientation.right() in self.predecessors:
                    for i in range(len(start)):
                        self.simulator.dependencies[(end[i], start[i])].extend(
                            self.get_end_of_predecessor(orientation.right()))
                # This car needs to leave the priority to the car on the right (so heading left)
                if orientation.left() in self.predecessors:
                    end_of_predecessor = self.get_end_of_predecessor(orientation.left())
                    for i in range(len(end_of_predecessor)):
                        self.simulator.dependencies[
                            (end_of_predecessor[i], self.get_start(orientation.left())[i])].extend(end)
