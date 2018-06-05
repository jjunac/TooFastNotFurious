from enum import IntEnum


class Orientation(IntEnum):
    NORTH = -90
    EAST = 0
    SOUTH = 90
    WEST = 180

    def right(self):
        return self.add(90)

    def invert(self):
        return self.add(180)

    def left(self):
        return self.add(270)

    def add(self, degree):
        return Orientation((self.value + degree) % 360)