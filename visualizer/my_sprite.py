import random

import pygame

from resources import ROAD_IMAGE, CAR_IMAGES
from visualizer.point import Point


class MySprite(pygame.sprite.Sprite):

    def __init__(self, pos, width=50, height=50, angle=0.0, image=None):
        pygame.sprite.Sprite.__init__(self)
        if not image.get_alpha():
            image = pygame.Surface.convert_alpha(image)
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.angle = 0
        self.rotate(angle)
        self.move_to(pos)

    def rotate(self, angle):
        """Rotate the image while keeping its center."""
        self.image = pygame.transform.rotate(self.image, angle - self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.angle = angle

    def move_to(self, pos):
        self.rect = self.rect.move(round(pos.x - self.image.get_rect().width / 2 - self.rect.x),
                                   round(pos.y - self.image.get_rect().height / 2 - self.rect.y))

    def move(self, pos):
        self.rect = self.rect.move(pos.x, pos.y)


class RoadSprite(MySprite):
    def __init__(self, pos, length=50, height=50, angle=0.0):
        super().__init__(pos, length, height, angle, ROAD_IMAGE)


class CarSprite(MySprite):

    def __init__(self, pos, car, length=50, height=50, angle=0.0):
        super().__init__(pos, length, height, angle, random.choice(CAR_IMAGES))
        self.car = car
        self.destination = None
        self.max_time = 15
        self.current_time = 0

    def update(self, *args):
        if self.destination:
            tick = args[0]
            self.current_time += 1
            if self.current_time >= self.max_time:
                print(self.rect, self.destination)
                # self.move_to(self.destination)²
                self.current_time = 0
                self.destination = None
            else:
                x = (self.destination.x - self.image.get_rect().width / 2 - self.rect.x) / self.max_time
                y = (self.destination.y - self.image.get_rect().height / 2 - self.rect.y) / self.max_time
                point = Point(x, y)
                self.move_to(point)

    def interpolate(self, start, destination):
        self.destination = destination
