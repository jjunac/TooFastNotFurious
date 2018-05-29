import pygame

from pygame.locals import *

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

    def f(self, x, coeff, d):
        return coeff * x + d

    def normale(self, c, coeff, d, x):

        an = -1 / coeff

        return int(self.f(c, coeff, d) + an * (x - c))

    def draw_road(self, x, y, xa, ya):

        if x > xa:
            x, xa = xa, x

        if y > ya:
            y, ya = ya, y

        d = 0

        coeff = 0

        if xa - x != 0:
            coeff = (ya - y) / (xa - x)

            d = y - (coeff * x)

        if (y == ya):

            pygame.draw.aaline(self.fenetre, BLACK, (x, y + HEIGHT / 2),
                               (xa, ya + HEIGHT / 2), True)
            pygame.draw.aaline(self.fenetre, BLACK, (x, y - HEIGHT / 2),
                               (xa, ya - HEIGHT / 2), True)

        elif coeff == 0:

            pygame.draw.aaline(self.fenetre, BLACK, (x - HEIGHT / 2, y),
                               (x - HEIGHT / 2, ya), True)
            pygame.draw.aaline(self.fenetre, BLACK, (x + HEIGHT / 2, y),
                               (x + HEIGHT / 2, ya), True)

        else:

            # pygame.draw.aaline(self.fenetre, BLACK, (x - HEIGHT / 2, y + HEIGHT / 2),
            #                    (xa - HEIGHT / 2, ya + HEIGHT / 2), True)
            # pygame.draw.aaline(self.fenetre, BLACK, (x + HEIGHT / 2, y - HEIGHT / 2),
            #                    (xa + HEIGHT / 2, ya - HEIGHT / 2), True)

            pygame.draw.aaline(self.fenetre, BLACK, (x - HEIGHT / 2, self.normale(x, coeff, d, x - HEIGHT / 2)),
                               (xa - HEIGHT / 2, self.normale(xa, coeff, d, xa - HEIGHT / 2)), True)
            pygame.draw.aaline(self.fenetre, BLACK, (x + HEIGHT / 2, self.normale(x, coeff, d, x + HEIGHT / 2)),
                               (xa + HEIGHT / 2, self.normale(xa, coeff, d, xa + HEIGHT / 2)), True)

        i = x

        if y == ya:

            while i < xa + 1:
                pygame.draw.aaline(self.fenetre, BLACK, (i, y + HEIGHT / 2),
                                   (i, y - HEIGHT / 2), True)

                i += WIDTH

        elif x == xa:

            i = y

            while i < ya + 1:
                pygame.draw.aaline(self.fenetre, BLACK, (x + HEIGHT / 2, i),
                                   (x - HEIGHT / 2, i), True)

                i += WIDTH

        else:

            pygame.draw.aaline(self.fenetre, BLACK, (x + HEIGHT / 2, self.normale(x, coeff, d, x + HEIGHT / 2)),
                               (x - HEIGHT / 2, self.normale(x, coeff, d, x - HEIGHT / 2)), True)

            while i < xa + 1:
                pygame.draw.aaline(self.fenetre, BLACK, (i + HEIGHT / 2, self.normale(i, coeff, d, i + HEIGHT / 2)),
                                   (i - HEIGHT / 2, self.normale(i, coeff, d, i - HEIGHT / 2)), True)

                i += WIDTH

    def draw(self):

        self.draw_road(100, 465, 500, 359)
        self.draw_road(100, 465, 365, 597)
        self.draw_road(100, 465, 984, 597)
        self.draw_road(100, 465, 100, 100)
        self.draw_road(100, 465, 500, 465)
        self.draw_road(0, 10, 1200, 10)

        pygame.display.flip()

        while self.continuer:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.continuer = 0


Drawing().draw()
