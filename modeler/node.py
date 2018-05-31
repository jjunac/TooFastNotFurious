from modeler.road import Road


class Node:

    def __init__(self):
        self.exits = {}
        self.entries = {}
        self.possible_destinations = {}

    def connect(self, orientation):
        r = Road(self, orientation)
        self.exits[orientation] = r
        return r
