import simulator
from modeler.junction_node import JunctionNode


class StopJunction(JunctionNode):

    def __init__(self):
        super().__init__()
        self.stop_orientation = None

    def with_stop_on_road(self, orientation):
        self.stop_orientation = orientation
        return self

    def build(self, sim):
        return simulator.StopJunction(sim, self.get_io_roads(), self.stop_orientation)
