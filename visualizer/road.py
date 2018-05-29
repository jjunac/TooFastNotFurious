import pygame


class SimpleRoad:

    def __init__(self, x, y, xa, ya):

        self.ya = ya
        self.xa = xa
        self.y = y
        self.x = x

    @staticmethod
    def f(x, a, b):
        return a * x + b

    @staticmethod
    def normal(c, coeff, d, x):
        an = -1 / coeff
        return int(SimpleRoad.f(c, coeff, d) + an * (x - c))

    def draw(self, surface, color=(0, 0, 0), height=30, width=30):
        if self.x > self.xa:
            self.x, self.xa = self.xa, self.x
        if self.y > self.ya:
            self.y, self.ya = self.ya, self.y
        d = 0
        coeff = 0
        if self.xa - self.x != 0:
            coeff = (self.ya - self.y) / (self.xa - self.x)
            d = self.y - (coeff * self.x)
        if self.y == self.ya:
            pygame.draw.aaline(surface, color, (self.x, self.y + height / 2), (self.xa, self.ya + height / 2),
                               True)
            pygame.draw.aaline(surface, color, (self.x, self.y - height / 2), (self.xa, self.ya - height / 2), True)
        elif coeff == 0:
            pygame.draw.aaline(surface, color, (self.x - height / 2, self.y), (self.x - height / 2, self.ya), True)
            pygame.draw.aaline(surface, color, (self.x + height / 2, self.y), (self.x + height / 2, self.ya), True)
        else:
            pygame.draw.aaline(surface, color,
                               (self.x - height / 2, self.normal(self.x, coeff, d, self.x - height / 2)),
                               (self.xa - height / 2, self.normal(self.xa, coeff, d, self.xa - height / 2)), True)
            pygame.draw.aaline(surface, color, (
                self.x + height / 2, self.normal(self.x, coeff, d, self.x + height / 2)),
                               (self.xa + height / 2, self.normal(self.xa, coeff, d, self.xa + height / 2)), True)
        i = self.x
        if self.y == self.ya:
            while i < self.xa + 1:
                pygame.draw.aaline(surface, color, (i, self.y + height / 2), (i, self.y - height / 2), True)
                i += width
        elif self.x == self.xa:
            i = self.y
            while i < self.ya + 1:
                pygame.draw.aaline(surface, color, (self.x + height / 2, i), (self.x - height / 2, i), True)
                i += width
        else:
            pygame.draw.aaline(surface, color, (
                self.x + height / 2, self.normal(self.x, coeff, d, self.x + height / 2)),
                               (self.x - height / 2, self.normal(self.x, coeff, d, self.x - height / 2)), True)
            while i < self.xa + 1:
                pygame.draw.aaline(surface, color, (i + height / 2, self.normal(i, coeff, d, i + height / 2)),
                                   (i - height / 2, self.normal(i, coeff, d, i - height / 2)), True)
                pygame.draw.aaline(surface, color, (i, self.f(i, coeff, d - height / 2)),
                                   (i, self.f(i, coeff, d + height / 2)), True)
                i += width
