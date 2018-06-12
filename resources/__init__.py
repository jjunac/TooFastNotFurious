import os

import pygame

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # This is your Project Root
JUNCTION4 = pygame.image.load(os.path.join(ROOT_DIR, "junction4.png"))
STOP_IMAGE = pygame.image.load(os.path.join(ROOT_DIR, "stop.png"))
ROAD_IMAGE = pygame.image.load(os.path.join(ROOT_DIR, "testRoad.png"))
CAR_IMAGES = []
for i in range(1, 9):
    CAR_IMAGES.append(pygame.image.load(os.path.join(ROOT_DIR, "car{0}.png".format(i))))
