from math import sqrt, cos, sin, pi


class Point:

    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def length(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    def rotate_point(self, degree_angle, point):
        radian_angle = to_radians(degree_angle)
        return Point(cos(radian_angle) * (point.x - self.x) - sin(radian_angle) * (point.y - self.y) + self.x,
                     sin(radian_angle) * (point.x - self.x) + cos(radian_angle) * (point.y - self.y) + self.y)


def to_radians(degree_angle):
    return degree_angle * pi / 180


def to_degrees(radian_angle):
    return radian_angle * 180 / pi
