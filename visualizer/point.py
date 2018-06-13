from math import sqrt, cos, sin, pi, isclose


class Point:

    def __init__(self, x, y):
        super().__init__()
        self.x = round(x)
        self.y = round(y)

    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        else:
            raise Exception

    def __add__(self, other):
        return Point(self.x + other[0], self.y + other[1])

    def __sub__(self, other):
        point = Point(self.x - other[0], self.y - other[1])
        return point

    def __mul__(self, other):
        return Point(self.x * other, self.y * other)

    def __truediv__(self, other):
        return Point(self.x / other, self.y / other)

    def length(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    def rotate_point(self, degree_angle, point):
        radian_angle = to_radians(degree_angle)
        return Point(cos(radian_angle) * (point[0] - self.x) - sin(radian_angle) * (point[1] - self.y) + self.x,
                     sin(radian_angle) * (point[0] - self.x) + cos(radian_angle) * (point[1] - self.y) + self.y)

    def __eq__(self, o):
        return isclose(o.x, self.x, abs_tol=1e-09) and isclose(o.y, self.y, abs_tol=1e-09)

    def __repr__(self):
        return "Point({0},{1})".format(self.x, self.y)

    def __str__(self) -> str:
        return "({0},{1})".format(self.x, self.y)

    def __neg__(self):
        return Point(-self.x, -self.y)


def to_radians(degree_angle):
    return degree_angle * pi / 180


def to_degrees(radian_angle):
    return radian_angle * 180 / pi
