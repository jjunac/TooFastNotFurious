from enum import IntEnum

class Orientation(IntEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def invert(self):
        return Orientation((self.value + 2) % 4)