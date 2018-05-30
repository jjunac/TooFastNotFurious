from modeler.road import Road


class Node:

    def __init__(self):
        self.exits = {}
        self.entries = {}

    def connect(self, orientation):
        r = Road(self, orientation)
        self.exits[orientation] = r
        return r
