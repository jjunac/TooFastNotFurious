from math import sqrt, cos, sin, atan2, pi

import pygame

from engine.state import State

road_image = pygame.image.load("../resources/testRoad.png")
car_image = pygame.image.load("../resources/car.png")


class SimpleRoad:

    def __init__(self, x, y, xa, ya):
        self.ya = ya
        self.xa = xa
        self.y = y
        self.x = x

    @staticmethod
    def f(x, a, b):
        return a * x + b

    @staticmethod
    def normal(c, coeff, d, x):
        an = -1 / coeff
        return int(SimpleRoad.f(c, coeff, d) + an * (x - c))

    def draw(self, surface, color=(0, 0, 0), height=30, width=30):
        if self.x > self.xa:
            self.x, self.xa = self.xa, self.x
        if self.y > self.ya:
            self.y, self.ya = self.ya, self.y
        d = 0
        coeff = 0
        if self.xa - self.x != 0:
            coeff = (self.ya - self.y) / (self.xa - self.x)
            d = self.y - (coeff * self.x)
        if self.y == self.ya:
            pygame.draw.aaline(surface, color, (self.x, self.y + height / 2), (self.xa, self.ya + height / 2),
                               True)
            pygame.draw.aaline(surface, color, (self.x, self.y - height / 2), (self.xa, self.ya - height / 2), True)
        elif coeff == 0:
            pygame.draw.aaline(surface, color, (self.x - height / 2, self.y), (self.x - height / 2, self.ya), True)
            pygame.draw.aaline(surface, color, (self.x + height / 2, self.y), (self.x + height / 2, self.ya), True)
        else:
            pygame.draw.aaline(surface, color,
                               (self.x - height / 2, self.normal(self.x, coeff, d, self.x - height / 2)),
                               (self.xa - height / 2, self.normal(self.xa, coeff, d, self.xa - height / 2)), True)
            pygame.draw.aaline(surface, color, (
                self.x + height / 2, self.normal(self.x, coeff, d, self.x + height / 2)),
                               (self.xa + height / 2, self.normal(self.xa, coeff, d, self.xa + height / 2)), True)
        i = self.x
        if self.y == self.ya:
            while i < self.xa + 1:
                pygame.draw.aaline(surface, color, (i, self.y + height / 2), (i, self.y - height / 2), True)
                i += width
        elif self.x == self.xa:
            i = self.y
            while i < self.ya + 1:
                pygame.draw.aaline(surface, color, (self.x + height / 2, i), (self.x - height / 2, i), True)
                i += width
        else:
            pygame.draw.aaline(surface, color, (
                self.x + height / 2, self.normal(self.x, coeff, d, self.x + height / 2)),
                               (self.x - height / 2, self.normal(self.x, coeff, d, self.x - height / 2)), True)
            while i < self.xa + 1:
                pygame.draw.aaline(surface, color, (i + height / 2, self.normal(i, coeff, d, i + height / 2)),
                                   (i - height / 2, self.normal(i, coeff, d, i - height / 2)), True)
                pygame.draw.aaline(surface, color, (i, self.f(i, coeff, d - height / 2)),
                                   (i, self.f(i, coeff, d + height / 2)), True)
                i += width


def rotate_point(angle, point, origin=(0, 0)):
    return (cos(angle) * (point[0] - origin[0]) - sin(angle) * (point[1] - origin[1]) + origin[0],
            sin(angle) * (point[0] - origin[0]) + cos(angle) * (point[1] - origin[1]) + origin[1])


class Road(pygame.sprite.Group):

    def __init__(self, x, y, xa, ya, car_group, length=30, height=30):
        super().__init__()
        self.x = x
        self.y = y
        self.xa = xa
        self.ya = ya
        self.car_group = car_group
        self.width = length
        self.height = height
        vect = (self.xa - self.x, self.ya - self.y)
        dist = sqrt(vect[0] ** 2 + vect[1] ** 2)
        self.angle = atan2(vect[1], vect[0])
        i = 0
        xtmp, ytmp = rotate_point(self.angle, (x + length, y), (x, y))
        self.xi = int(xtmp - x)
        self.yi = int(ytmp - y)
        while i < int(dist / length):
            road_portion = RoadSprite(x + self.xi * i, y + self.yi * i, length, height, self.angle)
            self.add(road_portion)
            i += 1
        if dist / length - i > 1:
            self.add(RoadSprite(x + self.xi * i, y + self.yi * i, int(dist - i * length), height, self.angle))

    def update(self, road_cells):
        index = 0
        self.car_group.clear()
        self.draw(pygame.display.get_surface())
        for cell in road_cells:
            if cell == State.CAR:
                car = MySprite(self.x + self.xi * index, self.y + self.yi * index, self.width, self.height,
                               self.angle, "car")
                self.car_group.add(car)
            index += 1
        self.car_group.draw(pygame.display.get_surface())


class MySprite(pygame.sprite.Sprite):

    def __init__(self, x=0, y=0, length=50, height=50, angle=0.0, image=None):
        pygame.sprite.Sprite.__init__(self)
        if not image.get_alpha():
            image = pygame.Surface.convert_alpha(image)
        image = pygame.transform.scale(image, (length, height))
        angle_degrees = -angle * 180 / pi
        self.image = pygame.transform.rotate(image, angle_degrees)
        point = rotate_point(-angle, (0, height))
        self.rect = image.get_rect().move(x - point[0], y)


class RoadSprite(MySprite):
    def __init__(self, x=0, y=0, length=50, height=50, angle=0.0):
        super().__init__(x, y, length, height, angle, road_image)
