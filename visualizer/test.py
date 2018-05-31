from math import cos, sin, pi

import pygame
from pygame.locals import *

from visualizer.junction import Junction
from visualizer.road import Road, MySprite
from visualizer.orientation import Orientation

HEIGHT = 7
WIDTH = 12

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Drawing:

    def __init__(self):
        pygame.init()
        self.fenetre = pygame.display.set_mode((1600, 900))
        self.fenetre.fill(WHITE)
        pygame.display.flip()
        self.continuer = 1

    def draw(self):
        r = Road(100, 100, 600, 100, None, length=50, height=50)
        r2 = Road(200, 0, 200, 400, None, length=50, height=50)
        r.draw(self.fenetre)
        r2.draw(self.fenetre)
        j = Junction(200, 500, None, length=50, height=50)
        j1 = Junction(400, 500, None, 3, Orientation.SOUTH, length=50, height=50)
        j2 = Junction(600, 500, None, 3, Orientation.NORTH, length=50, height=50)
        j3 = Junction(800, 500, None, 3, Orientation.EAST, length=50, height=50)
        j4 = Junction(1000, 500, None, 3, Orientation.WEST, length=50, height=50)
        j.draw(self.fenetre)
        j1.draw(self.fenetre)
        j2.draw(self.fenetre)
        j3.draw(self.fenetre)
        j4.draw(self.fenetre)
        clear = pygame.sprite.RenderClear()
        # clear.add(RoadSprite(100, 100, 50, 50, pi/4))
        clear.draw(pygame.display.get_surface())
        pygame.draw.circle(self.fenetre, (255, 0, 0), (100, 100), 10)
        pygame.draw.circle(self.fenetre, (255, 0, 0), (0, 0), 10)
        pygame.draw.circle(self.fenetre, (255, 0, 0), (200, 400), 10)
        pygame.draw.circle(self.fenetre, (255, 0, 0), (400, 500), 10)
        pygame.draw.circle(self.fenetre, (255, 0, 0), (600, 500), 10)
        pygame.draw.circle(self.fenetre, (255, 0, 0), (800, 500), 10)
        pygame.draw.circle(self.fenetre, (255, 0, 0), (1000, 500), 10)
        pygame.display.flip()
        while self.continuer:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.continuer = 0


Drawing().draw()