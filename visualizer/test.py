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

        # Prendre le coeff inverse

        d = 0

        coeff = 0

        if xa - x != 0:
            coeff = (ya - y) / (xa - x)

            d = y - (coeff * x)

        # an = -1 / coeff
        #
        # normale = self.f(x, coeff, d) + an * (x - x)

        # pygame.draw.circle(self.fenetre, BLACK, [x, int(normale)], 4, 2)

        pygame.draw.aaline(self.fenetre, BLACK, (x + HEIGHT / 2, self.normale(x, coeff, d, x + HEIGHT / 2)),
                           (x - HEIGHT / 2, self.normale(x, coeff, d, x - HEIGHT / 2)), True)

        if (y == ya):

            pygame.draw.aaline(self.fenetre, BLACK, (x, y + HEIGHT / 2),
                               (xa, ya + HEIGHT / 2), True)
            pygame.draw.aaline(self.fenetre, BLACK, (x, y - HEIGHT / 2),
                               (xa, ya - HEIGHT / 2), True)

        else:

            pygame.draw.aaline(self.fenetre, BLACK, (x - HEIGHT / 2, y + HEIGHT / 2),
                               (xa - HEIGHT / 2, ya + HEIGHT / 2), True)
            pygame.draw.aaline(self.fenetre, BLACK, (x + HEIGHT / 2, y - HEIGHT / 2),
                               (xa + HEIGHT / 2, ya - HEIGHT / 2), True)

        i = x

        while i < xa + 1:
            # pygame.draw.aaline(self.fenetre, BLACK, (i + HEIGHT / 2, coeff * i + d - HEIGHT / 2),
            #                    (i - HEIGHT / 2, coeff * i + d + HEIGHT / 2), True)
            # pygame.draw.aaline(self.fenetre, BLACK, (i  , self.f(i , coeff, d)),
            #                    (i, self.f(i, coeff, d)), True)
            pygame.draw.aaline(self.fenetre, BLACK, (i + HEIGHT / 2, self.normale(i, coeff, d, i + HEIGHT / 2)),
                               (i - HEIGHT / 2, self.normale(i, coeff, d, i - HEIGHT / 2)), True)

            i += WIDTH

    def draw(self):

        self.draw_road(100, 465, 500, 359)
        self.draw_road(100, 465, 365, 597)
        self.draw_road(100, 465, 984, 597)
        self.draw_road(100, 465, 100, 100)
        self.draw_road(100, 465, 500, 465)
        # self.draw_road(0, 10, 1200, 10)

        pygame.display.flip()

        while self.continuer:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.continuer = 0


Drawing().draw()
