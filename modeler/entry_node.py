from modeler.path import Path
from modeler.node import Node
import simulator

class EntryNode(Node):

    def __init__(self):
        super().__init__()


    def go_through(self, *junctions):
        p = Path(self)
        p.junctions = junctions
        return p


    def build(self):
        """paths = {}
        total_proportion = 0
        for proportion, path in self.paths:
            total_proportion ++ proportion/100
            directions = [0] * self.possible_destinations[path[0]]
            for i in range(len(path)-1):
                directions.append(path[i].possible_destinations.index(path[i+1]))
                directions.extend([0] * path[i].possible_destinations[path[i + 1]])
            paths[total_proportion + proportion] = path"""
        return simulator.EntryNode(0.5)