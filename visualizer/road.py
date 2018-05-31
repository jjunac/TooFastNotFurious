from math import sqrt, cos, sin, atan2, pi

import pygame

from resources import CAR_IMAGE, ROAD_IMAGE


def rotate_point(angle, point, origin=(0, 0)):
    return (cos(angle) * (point[0] - origin[0]) - sin(angle) * (point[1] - origin[1]) + origin[0],
            sin(angle) * (point[0] - origin[0]) + cos(angle) * (point[1] - origin[1]) + origin[1])


class GraphicRoad(pygame.sprite.Group):

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
        i = 1
        xtmp, ytmp = rotate_point(self.angle, (self.x + length, self.y), (self.x, self.y))
        self.xi = int(xtmp - self.x)
        self.yi = int(ytmp - self.y)
        angle_degree = self.angle * 180 / pi
        while i < int(dist / length):
            road_portion = RoadSprite(self.x + self.xi * i, self.y + self.yi * i, length, height, angle_degree)
            self.add(road_portion)
            i += 1
        if dist / length - i > 1:
            self.add(
                RoadSprite(self.x + self.xi * i, self.y + self.yi * i, int(dist - i * length), height, angle_degree))

    def update(self, road_cells):
        pass
        # index = 0
        # # self.car_group.clear(pygame.display.get_surface(), pygame.display.get_surface())
        # self.car_group.empty()
        # self.draw(pygame.display.get_surface())
        # for cell in road_cells:
        #     if cell == State.CAR:
        #         car = CarSprite(self.x + self.xi * index, self.y + self.yi * index, self.cell_length, self.height,
        #                         self.angle_degree)
        #         self.car_group.add(car)
        #     index += 1
        # self.car_group.draw(pygame.display.get_surface())


class MySprite(pygame.sprite.Sprite):

    def __init__(self, x=0, y=0, length=50, height=50, angle=0.0, image=None):
        print(str(x) + " " + str(y) + str(angle))
        pygame.sprite.Sprite.__init__(self)
        if not image.get_alpha():
            image = pygame.Surface.convert_alpha(image)
        image = pygame.transform.scale(image, (length, height))
        rect = image.get_rect().move(x - image.get_rect().width / 2, y - image.get_rect().height / 2)
        self.image, self.rect = MySprite.rotate(image, rect, angle)

    @staticmethod
    def rotate(image, rect, angle):
        """Rotate the image while keeping its center."""
        # Rotate the original image without modifying it.
        new_image = pygame.transform.rotate(image, angle)
        # Get a new rect with the center of the old rect.
        rect = new_image.get_rect(center=rect.center)
        return new_image, rect


class RoadSprite(MySprite):
    def __init__(self, x=0, y=0, length=50, height=50, angle=0.0):
        super().__init__(x, y, length, height, angle, ROAD_IMAGE)


class CarSprite(MySprite):
    def __init__(self, x=0, y=0, length=50, height=50, angle=0.0):
        super().__init__(x, y, length, height, angle, CAR_IMAGE)
