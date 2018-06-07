from math import sqrt, cos, sin, pi, isclose


class Point:

    def __init__(self, x, y):
        super().__init__()
        self.x = round(x)
        self.y = round(y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        point = Point(self.x - other.x, self.y - other.y)
        return point

    def __mul__(self, other):
        return Point(self.x * other, self.y * other)

    def __truediv__(self, other):
        return Point(self.x / other, self.y / other)

    def length(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    def rotate_point(self, degree_angle, point):
        radian_angle = to_radians(degree_angle)
        return Point(cos(radian_angle) * (point.x - self.x) - sin(radian_angle) * (point.y - self.y) + self.x,
                     sin(radian_angle) * (point.x - self.x) + cos(radian_angle) * (point.y - self.y) + self.y)

    def __eq__(self, o):
        return isclose(o.x, self.x, abs_tol=1e-09) and isclose(o.y, self.y, abs_tol=1e-09)

    def __str__(self) -> str:
        return "({0},{1})".format(self.x, self.y)

    def __neg__(self):
        return Point(-self.x, -self.y)


def to_radians(degree_angle):
    return degree_angle * pi / 180


def to_degrees(radian_angle):
    return radian_angle * 180 / pi
