import pygame

from resources import JUNCTION4


class JunctionSprite(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0, length=50, height=50, angle=0.0, image=JUNCTION4):
        pygame.sprite.Sprite.__init__(self)
        if not image.get_alpha():
            image = pygame.Surface.convert_alpha(image)
        image = pygame.transform.scale(image, (length, height))
        self.image = pygame.transform.rotate(image, angle)
        self.rect = image.get_rect().move(x, y)
