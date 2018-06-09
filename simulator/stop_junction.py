from simulator.junction import Junction


class StopJunction(Junction):

    def __init__(self, simulator, io_roads, orientation_stop):
        super().__init__(simulator, io_roads)
        self.orientation_stop = orientation_stop

    def do_add_predecessor(self, orientation, predecessor):
        super().do_add_predecessor(orientation, predecessor)
        end = predecessor.get_end(orientation.invert())
        start = self.get_start(orientation.invert())

        if orientation == self.orientation_stop:
            for o in self.predecessors.keys():
                if o == orientation.invert():
                    continue
                for i in range(len(start)):
                    self.simulator.dependencies[(end[i], start[i])].extend(self.get_end_of_predecessor(o))
        else:
            if self.orientation_stop.invert() in self.predecessors:
                end_of_predecessor = self.get_end_of_predecessor(self.orientation_stop.invert())
                stop_start = self.get_start(self.orientation_stop.invert())
                for i in range(len(end_of_predecessor)):
                    self.simulator.dependencies[(end_of_predecessor[i], stop_start[i])].extend(end)
