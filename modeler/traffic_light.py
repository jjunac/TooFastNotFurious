import simulator
from modeler.junction_node import JunctionNode


class TrafficLight(JunctionNode):

    def __init__(self):
        super().__init__()
        self.__state_indicator = 0
        self.state1_orientations = []
        self.state1_timer = 0
        self.state2_orientations = []
        self.state2_timer = 0
        self.interval = 0

    def set_state1_orientations(self, *orientations):
        self.state1_orientations = orientations
        self.__state_indicator = 1
        return self

    def set_state2_orientations(self, *orientations):
        self.state2_orientations = orientations
        self.__state_indicator = 2
        return self

    def with_timer(self, timer):
        if self.__state_indicator == 1:
            self.state1_timer = timer
        elif self.__state_indicator == 2:
            self.state2_timer = timer
        return self

    def with_interval(self, interval):
        self.interval = interval
        return self

    def build(self, sim):
        return simulator.TrafficLightJunction(sim, self.get_io_roads(), self.state1_orientations, self.state1_timer, self.state2_orientations, self.state2_timer, self.interval)