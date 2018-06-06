import pygame

from resources import ROAD_IMAGE, CAR_IMAGE


class MySprite(pygame.sprite.Sprite):

    def __init__(self, pos, width=50, height=50, angle=0.0, image=None):
        pygame.sprite.Sprite.__init__(self)
        if not image.get_alpha():
            image = pygame.Surface.convert_alpha(image)
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.move(pos)
        self.angle = 0
        self.rotate(angle)

    def rotate(self, angle):
        """Rotate the image while keeping its center."""
        self.image = pygame.transform.rotate(self.image, angle - self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.angle = angle

    def move(self, pos):
        self.rect = self.rect.move(round(pos.x - self.image.get_rect().width / 2 - self.rect.x),
                                   round(pos.y - self.image.get_rect().height / 2 - self.rect.y))


class RoadSprite(MySprite):
    def __init__(self, pos, length=50, height=50, angle=0.0):
        super().__init__(pos, length, height, angle, ROAD_IMAGE)


class CarSprite(MySprite):
    def __init__(self, pos, car, length=50, height=50, angle=0.0):
        super().__init__(pos, length, height, angle, CAR_IMAGE)
        self.car = car
