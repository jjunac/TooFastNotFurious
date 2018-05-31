from math import cos, sin, pi

import pygame
from pygame.locals import *

from visualizer.junction import Junction
from visualizer.road import Road, MySprite
from visualizer.orientation import Orientation
from engine.state import State

HEIGHT = 7
WIDTH = 12

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Mock:

    def __init__(self):
        pygame.init()
        self.fenetre = pygame.display.set_mode((1600, 900))
        self.fenetre.fill(WHITE)
        pygame.display.flip()
        self.continuer = 1
        self.r = Road(100, 100, 600, 100, pygame.sprite.Group(), length=50, height=50)
        self.clock = pygame.time.Clock()

    def draw(self):

        cells = [State.EMPTY, State.EMPTY, State.CAR, State.EMPTY, State.EMPTY, State.EMPTY, State.EMPTY, State.EMPTY,
                 State.EMPTY, State.EMPTY]

        # r2 = Road(200, 0, 200, 400, None, length=50, height=50)
        self.r.draw(self.fenetre)
        # r2.draw(self.fenetre)

        clear = pygame.sprite.RenderClear()
        # clear.add(RoadSprite(100, 100, 50, 50, pi/4))
        clear.draw(pygame.display.get_surface())
        pygame.draw.circle(self.fenetre, (255, 0, 0), (100, 100), 10)

        pygame.display.flip()
        while self.continuer:

            self.r.update(cells)

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.continuer = 0
            pygame.display.update()
            self.clock.tick(3)
            self.maj_cells(cells)

    def maj_cells(self, cells):

        for i in range(-1, -len(cells) + 1, -1):
            print("Indice", i)
            if cells[i - 1] == State.CAR:
                cells[i] = State.CAR
            else:
                cells[i] = State.EMPTY


Mock().draw()
