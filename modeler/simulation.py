import simulator
from simulator.simulator import Simulator

class Simulation:

    def __init__(self):
        self.built_entities = []
        self.node_conversion = {}
        self.nodes = []
        self.roads = []
        self.paths = []
        self.simulator = Simulator()



    def __build_node(self, node):
        build = node.build(self.simulator)
        self.node_conversion[node] = build
        self.built_entities.append(build)


    def __build_road(self, road):
        build = road.build(self.simulator)

        # Link the start
        start_build = self.node_conversion[road.start]
        build.add_predecessor(road.orientation, start_build)
        # Link the end
        end_build = self.node_conversion[road.end]
        end_build.add_predecessor(road.orientation, build)

        self.built_entities.remove(end_build)
        self.built_entities.append(build)
        self.built_entities.append(end_build)


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
        self.simulator.run(ticks)


    def run_graphical_for(self, ticks):
        self.__build_all()
        self.simulator.run_graphical(ticks)

