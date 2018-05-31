import pygame

from resources import JUNCTION3, JUNCTION4

HEIGHT = 7
WIDTH = 12
WIDTH_LINE = 2

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Junction(pygame.sprite.Group):

    def __init__(self, x, y, car_group, nb_entries=4, orientation=0, length=30, height=30):
        super().__init__()
        self.x = x
        self.y = y
        self.car_group = car_group
        self.nb_entries = nb_entries
        self.orientation = orientation
        self.width = length
        self.height = height

        if nb_entries == 4:
            self.add(JunctionSprite(x, y, self.width, self.height))

        else:

            self.add(JunctionSprite(x, y, self.width, self.height, orientation, JUNCTION3))

    def update(self, junction_entity):

        print("coucou")


class JunctionSprite(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0, length=50, height=50, angle=0.0, image=JUNCTION4):
        pygame.sprite.Sprite.__init__(self)
        if not image.get_alpha():
            image = pygame.Surface.convert_alpha(image)
        image = pygame.transform.scale(image, (length, height))
        self.image = pygame.transform.rotate(image, angle)
        self.rect = image.get_rect().move(x, y)
