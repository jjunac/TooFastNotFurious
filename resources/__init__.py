import os

import pygame

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # This is your Project Root
JUNCTION4 = pygame.image.load(os.path.join(ROOT_DIR, "junction4.png"))
JUNCTION3 = pygame.image.load(os.path.join(ROOT_DIR, "junction3.png"))
ROAD_IMAGE = pygame.image.load(os.path.join(ROOT_DIR, "testRoad.png"))
CAR_IMAGE = pygame.image.load(os.path.join(ROOT_DIR, "car.png"))