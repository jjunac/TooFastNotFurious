import pygame

from pygame.locals import *

from visualizer.orientation import Orientation

HEIGHT = 7
WIDTH = 12
WIDTH_LINE = 2

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Junction:

    def __init__(self):
        pygame.init()
        self.fenetre = pygame.display.set_mode((1600, 900))
        self.fenetre.fill(WHITE)

        pygame.display.flip()

        self.continuer = 1

    def draw_junction(self, x, y, nb_entries, orientation=0):

        if nb_entries == 4:

            pygame.draw.line(self.fenetre, BLACK, (x - WIDTH * 1.5, y),
                               (x + WIDTH * 1.5, y), WIDTH_LINE)
            pygame.draw.line(self.fenetre, BLACK, (x, y - WIDTH * 1.5),
                               (x, y + WIDTH * 1.5), WIDTH_LINE)

        else:

            if orientation == Orientation.NORTH:

                pygame.draw.line(self.fenetre, BLACK, (x - WIDTH * 1.5, y),
                                   (x + WIDTH * 1.5, y), WIDTH_LINE)
                pygame.draw.line(self.fenetre, BLACK, (x, y - WIDTH * 1.5),
                                   (x, y), WIDTH_LINE)

            elif orientation == Orientation.SOUTH:

                pygame.draw.line(self.fenetre, BLACK, (x - WIDTH * 1.5, y),
                                   (x + WIDTH * 1.5, y), WIDTH_LINE)
                pygame.draw.line(self.fenetre, BLACK, (x, y),
                                   (x, y + WIDTH * 1.5), WIDTH_LINE)

            elif orientation == Orientation.EAST:

                pygame.draw.line(self.fenetre, BLACK, (x, y),
                                   (x + WIDTH * 1.5, y), WIDTH_LINE)
                pygame.draw.line(self.fenetre, BLACK, (x, y - WIDTH * 1.5),
                                   (x, y + WIDTH * 1.5), WIDTH_LINE)

            else:

                pygame.draw.line(self.fenetre, BLACK, (x - WIDTH * 1.5, y),
                                   (x, y), WIDTH_LINE)
                pygame.draw.line(self.fenetre, BLACK, (x, y - WIDTH * 1.5),
                                   (x, y + WIDTH * 1.5), WIDTH_LINE)

    def draw(self):

        self.draw_junction(50, 50, 4)
        self.draw_junction(100, 50, 3, Orientation.NORTH)
        self.draw_junction(150, 50, 3, Orientation.EAST)
        self.draw_junction(200, 50, 3, Orientation.WEST)
        self.draw_junction(250, 50, 3, Orientation.SOUTH)
        pygame.display.flip()

        while self.continuer:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.continuer = 0


Junction().draw()
