import pygame

from resources import ROAD_IMAGE, CAR_IMAGE


class MySprite(pygame.sprite.Sprite):

    def __init__(self, pos, length=50, height=50, angle=0.0, image=None):
        pygame.sprite.Sprite.__init__(self)
        if not image.get_alpha():
            image = pygame.Surface.convert_alpha(image)
        image = pygame.transform.scale(image, (length, height))
        rect = image.get_rect().move(pos.x - image.get_rect().width / 2, pos.y - image.get_rect().height / 2)
        self.image, self.rect = MySprite.rotate(image, rect, angle)

    @staticmethod
    def rotate(image, rect, angle):
        """Rotate the image while keeping its center."""
        new_image = pygame.transform.rotate(image, angle)
        rect = new_image.get_rect(center=rect.center)
        return new_image, rect


class RoadSprite(MySprite):
    def __init__(self, pos, length=50, height=50, angle=0.0):
        super().__init__(pos, length, height, angle, ROAD_IMAGE)


class CarSprite(MySprite):
    def __init__(self, pos, length=50, height=50, angle=0.0):
        super().__init__(pos, length, height, angle, CAR_IMAGE)
