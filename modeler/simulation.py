from simulator.utils import build_road
from simulator.simulator import Simulator

class Simulation:

    def __init__(self):
        self.nodes = []
        self.node_conversion = {}


    def add_node(self, node):
        build = node.build()
        self.node_conversion[node] = build
        self.nodes.append(build)
        return self


    def add_road(self, road):
        build = build_road(road.length)

        # Link the start
        start_build = self.node_conversion[road.start]
        start_build.successors.append(build[0])
        build[0].predecessors.append(start_build)
        # Link the end
        end_build = self.node_conversion[road.end]
        end_build.predecessors.append(build[-1])
        build[-1].successors.append(end_build)

        self.nodes.remove(end_build)
        self.nodes.extend(build)
        self.nodes.append(end_build)
        return self


    def run_for(self, ticks):
        s = Simulator(self.nodes)
        s.run(ticks)
