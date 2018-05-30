from math import sqrt, cos, sin, atan2, pi

import pygame

from engine.state import State

road_image = pygame.image.load("../resources/testRoad.png")
car_image = pygame.image.load("../resources/car.png")


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
                car = CarSprite(self.x + self.xi * index, self.y + self.yi * index, self.width, self.height,
                                self.angle)
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


class CarSprite(MySprite):
    def __init__(self, x=0, y=0, length=50, height=50, angle=0.0):
        super().__init__(x, y, length, height, angle, car_image)
