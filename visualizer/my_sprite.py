import random
from math import atan2

import pygame

from resources import ROAD_IMAGE, CAR_IMAGES
from visualizer.point import Point, to_degrees


class MySprite(pygame.sprite.Sprite):

    def __init__(self, pos, width=50, height=50, angle=0.0, image=None):
        pygame.sprite.Sprite.__init__(self)
        if not image.get_alpha():
            image = pygame.Surface.convert_alpha(image)
        self.baseImage = pygame.transform.scale(image, (width, height))
        self.image = None
        self.rect = self.baseImage.get_rect()
        self.angle = 0
        self.rotate(angle)
        self.move_to(pos)

    def rotate(self, angle):
        """Rotate the image while keeping its center."""
        self.image = pygame.transform.rotate(self.baseImage, angle)
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
        self.start_angle = self.angle
        self.car = car
        self.destination = None
        self.max_time = 15
        self.current_time = 0
        self.delta = Point(0, 0)
        self.start = None

    def update(self, *args):
        if self.destination:
            self.current_time += 1
            if self.current_time >= self.max_time:
                self.current_time = 0
                self.move_to(self.destination)
                if self.destination != self.start:
                    degrees = -to_degrees(atan2(self.destination.y - self.start.y, self.destination.x - self.start.x))
                    self.rotate(degrees)
                self.destination = None
            else:
                self.rotate(self.start_angle)
                point = self.delta * self.current_time + self.start
                self.move_to(point)

    def interpolate(self, destination):
        self.start = Point(self.rect.x + self.image.get_rect().width / 2,
                           self.rect.y + self.image.get_rect().height / 2)
        if self.start != destination:
            self.destination = destination
            self.delta = Point((self.destination.x - self.start.x) / self.max_time,
                               (self.destination.y - self.start.y) / self.max_time)
            degrees = self.good_angle(
                -to_degrees(atan2(self.destination.y - self.start.y, self.destination.x - self.start.x)))
            self.start_angle = degrees

    @staticmethod
    def good_angle(angle):
        return (360 + angle) % 360
