import pygame
from pygame.locals import *

from visualizer.road import SimpleRoad

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

    def normale(self, c, coeff, d, x):

        an = -1 / coeff
        return int(f(c, coeff, d) + an * (x - c))

    def draw(self):
        # road = RoadSprite()
        # road.image = pygame.transform.rotate(road.image, 30)
        render_clear = pygame.sprite.RenderClear()
        # render_clear.add(road)
        render_clear.draw(self.fenetre)
        # r = Road(0, 0, 400, 0, render_clear)
        road2 = SimpleRoad(205, 200, 260, 454)
        road2.draw(self.fenetre)
        pygame.display.flip()

        while self.continuer:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.continuer = 0


Drawing().draw()
