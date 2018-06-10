from simulator.junction import Junction


class TrafficLightJunction(Junction):

    def __init__(self, simulator, io_roads, state1_orientations, state1_timer, state2_orientations, state2_timer, interval):
        super().__init__(simulator, io_roads)
        self.state1_orientations = state1_orientations
        self.state1_timer = state1_timer
        self.state2_orientations = state2_orientations
        self.state2_timer = state2_timer
        self.interval = interval
        self.total_time = state1_timer + interval + state2_timer + interval
        self.counter = 0

    def apply_next(self):
        super().apply_next()
        self.counter += 1

    def is_dependency_satisfied(self, source):
        if source in self.get_nodes():
            return True

        orientations = None
        if self.counter < self.state1_timer:
            orientations = self.state1_orientations
        elif self.counter < self.state1_timer + self.interval:
            return False
        elif self.counter < self.state1_timer + self.interval + self.state2_timer:
            orientations = self.state2_orientations
        else:
            return False

        for o in orientations:
            if source in self.predecessors[o].get_end(o.invert()):
                return True
        return False