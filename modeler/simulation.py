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


    def add_path(self, path):
        node = self.node_conversion[path.departure]
        directions = [0] * (path.departure.possible_destinations[path.junctions[0]] + 1)
        for i in range(len(path.junctions) - 1):
            directions.append(path.junctions[i].possible_destinations.index(path.junctions[i + 1]))
            directions.extend([0] * path.junctions[i].possible_destinations[path.junctions[i + 1]])
        total_proportion = max(node.paths.keys()) if len(node.paths) >= 1 else 0
        node.paths[total_proportion + path.proportion] = simulator.Path(directions)


    def run_for(self, ticks):
        s = Simulator(self.nodes)
        s.run(ticks)
