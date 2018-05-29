from math import cos, sin, pi

import pygame
from pygame.locals import *
from visualizer.road import SimpleRoad

HEIGHT = 7
WIDTH = 12

BLACK = (0, 0, 0)
RED = (220, 0, 0)
WHITE = (255, 255, 255)


def f(x, a, b):
    return a * x + b


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
        road = SimpleRoad(100, 465, 400, 465)
        road.draw(self.fenetre)
        road2 = SimpleRoad(205, 200, 260, 454)
        road2.draw(self.fenetre)
        pygame.display.flip()

        while self.continuer:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.continuer = 0


class RotatableRect:
    def __init__(self, xpos, ypos, width, height, angle):
        self.height = height
        self.xpos = xpos
        self.ypos = ypos
        self.width = width
        self.angle = angle

    def draw(self, surface, color):
        b_l = (self.xpos, self.ypos)
        b_r = self.__rotatePoint((b_l[0] + self.width), b_l)
        t_r = (self.xpos + self.width, self.ypos + self.height)
        t_l = (self.xpos, self.ypos + self.height)
        pygame.draw.aaline(surface, color, (self.xpos, self.ypos), self.__rotatePoint(b_l, b_r))
        pygame.draw.aaline(surface, color, b_r, self.__rotatePoint(b_r, t_r))
        pygame.draw.aaline(surface, color, t_r, self.__rotatePoint(t_r, t_l))
        pygame.draw.aaline(surface, color, t_l, self.__rotatePoint(t_l, b_l))

    def __rotateLine(self, origin, line):
        point = self.__rotatePoint(origin, line[0])
        self.__rotatePoint(origin, line[1])

    def __rotatePoint(self, point, origin=(0, 0)):
        return (cos(self.angle) * (point[0] - origin[0]) - sin(self.angle) * (point[1] - origin[1]) + origin[0],
                sin(self.angle) * (point[0] - origin[0]) + cos(self.angle) * (point[1] - origin[1]) + origin[1])

    def rotate(self, angle):
        self.angle = angle


if __name__ == '__main__':
    Drawing().draw()
