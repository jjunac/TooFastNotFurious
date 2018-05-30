import pygame

from pygame.locals import *

from visualizer.orientation import Orientation
from visualizer.road import rotate_point

HEIGHT = 7
WIDTH = 12
WIDTH_LINE = 2

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

junction4 = pygame.image.load("../resources/junction4.png")
junction3 = pygame.image.load("../resources/junction3.png")


class Junction(pygame.sprite.Group):

    def __init__(self, x, y, car_group, nb_entries=4, orientation=0, length=30, height=30):
        super().__init__()
        self.x = x
        self.y = y
        self.car_group = car_group
        self.nb_entries = nb_entries
        self.orientation = orientation

        if nb_entries == 4:
            self.width = length * 3
            self.height = height * 3
            self.add(JunctionSprite(x, y, self.width, self.height))

        else:

            if orientation == Orientation.NORTH:
                self.width = length * 3
                self.height = height * 2
                self.add(JunctionSprite(x, y, self.width, self.height, 180.0, junction3))

            elif orientation == Orientation.SOUTH:
                self.width = length * 3
                self.height = height * 2
                self.add(JunctionSprite(x, y, self.width, self.height, image=junction3))

            elif orientation == Orientation.EAST:
                self.width = length * 3
                self.height = height * 2
                self.add(JunctionSprite(x, y, self.width, self.height, 270, junction3))

            else:
                self.width = length * 3
                self.height = height * 2
                self.add(JunctionSprite(x, y, self.width, self.height, 90, junction3))

    def update(self, junction_entity):

        print("coucou")


class JunctionSprite(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0, length=150, height=150, angle=0.0, image=junction4):
        pygame.sprite.Sprite.__init__(self)
        if not image.get_alpha():
            image = pygame.Surface.convert_alpha(image)
        image = pygame.transform.scale(image, (length, height))
        self.image = pygame.transform.rotate(image, angle)
        self.rect = image.get_rect().move(x, y)
