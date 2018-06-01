import simulator
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
        build = road.build()

        # Link the start
        start_build = self.node_conversion[road.start]
        simulator.link(start_build, build[0])
        # Link the end
        end_build = self.node_conversion[road.end]
        simulator.link(build[-1], end_build)

        self.nodes.remove(end_build)
        self.nodes.extend(build)
        self.nodes.append(end_build)
        return self


    def add_path(self, path):
        node = self.node_conversion[path.departure]
        directions = [0] * (path.departure.possible_destinations[path.junctions[0]][1] + 1)
        for i in range(len(path.junctions) - 1):
            index, length = path.junctions[i].possible_destinations[path.junctions[i + 1]]
            directions.append(index)
            directions.extend([0] * length)
        total_proportion = max(node.paths.keys()) if len(node.paths) >= 1 else 0
        node.paths[total_proportion + path.proportion] = simulator.Path(directions)


    def run_for(self, ticks):
        s = Simulator(self.nodes)
        s.run(ticks)

    def run_graphical_for(self, ticks):
        s = Simulator(self.nodes)
        s.run_graphical(ticks)
