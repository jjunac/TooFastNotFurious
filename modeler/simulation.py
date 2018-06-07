import simulator
from simulator import Path
from simulator.simulator import Simulator
from shared import dijkstra, reconstruct_path

class Simulation:

    def __init__(self):
        self.entity_conversion = {}
        self.nodes = []
        self.roads = []
        self.paths = []
        self.simulator = Simulator()

    def with_report(self):
        self.simulator.generate_report()

    def __build_node(self, node):
        build = node.build(self.simulator)
        self.entity_conversion[node] = build


    def __build_road(self, road):
        build = road.build(self.simulator)

        # Link the start
        start_build = self.entity_conversion[road.start]
        build.add_predecessor(road.orientation, start_build)
        # Link the end
        end_build = self.entity_conversion[road.end]
        end_build.add_predecessor(road.orientation, build)


    def __build_path(self, path):
        entry = self.entity_conversion[path.departure]
        exit = self.entity_conversion[path.destination]

        paths = []

        for n in entry.get_nodes():
            res = dijkstra(self.simulator.get_nodes(), n)
            paths.append(Path(reconstruct_path(res, n, min(exit.get_nodes(), key=lambda e:res[e]))))

        total_proportion = max(entry.paths.keys()) if len(entry.paths) >= 1 else 0
        entry.paths[total_proportion + path.proportion] = paths


    def build_all(self):
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
        self.build_all()
        self.simulator.run(ticks)


    def run_graphical_for(self, ticks):
        self.build_all()
        self.simulator.run_graphical(ticks)

