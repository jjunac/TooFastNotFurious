import simulator
from simulator.simulator import Simulator

class Simulation:

    def __init__(self):
        self.built_nodes = []
        self.node_conversion = {}
        self.nodes = []
        self.roads = []
        self.paths = []
        self.dependencies = {}


    def __build_node(self, node):
        build = node.build()
        self.node_conversion[node] = build
        self.built_nodes.append(build)


    def __build_road(self, road):
        build = road.build()

        # Link the start
        start_build = self.node_conversion[road.start]
        simulator.link(start_build, build[0])
        # Link the end
        end_build = self.node_conversion[road.end]
        simulator.link(build[-1], end_build)



        self.built_nodes.remove(end_build)
        self.built_nodes.extend(build)
        self.built_nodes.append(end_build)


    def __build_path(self, path):
        node = self.node_conversion[path.departure]
        directions = [0] * (path.departure.possible_destinations[path.junctions[0]][1] + 1)
        for i in range(len(path.junctions) - 1):
            index, length = path.junctions[i].possible_destinations[path.junctions[i + 1]]
            directions.append(index)
            directions.extend([0] * length)
        total_proportion = max(node.paths.keys()) if len(node.paths) >= 1 else 0
        node.paths[total_proportion + path.proportion] = simulator.Path(directions)


    def __build_all(self):
        for n in self.nodes:
            self.__build_node(n)
        for r in self.roads:
            self.__build_road(r)
        for p in self.paths:
            self.__build_path(p)


    def add_node(self, node):
        self.nodes.append(node)


    def add_road(self, road):
        self.roads.append(road)
        
        
    def add_path(self, path):
        self.paths.append(path)


    def run_for(self, ticks):
        self.__build_all()
        s = Simulator(self.built_nodes)
        s.run(ticks)


    def run_graphical_for(self, ticks):
        self.__build_all()
        s = Simulator(self.built_nodes)
        s.run_graphical(ticks)

