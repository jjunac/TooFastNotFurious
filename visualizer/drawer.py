import time
from copy import copy

import pygame
from pygame.locals import *

from simulator.road import Road
from visualizer.point import Point
from visualizer.road import GraphicRoad

HEIGHT = 7
WIDTH = 12

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Drawer:

    def __init__(self, simulator, width=1280, height=720, cell_height=30, cell_length=30):
        self.height = height
        self.width = width
        self.cell_length = cell_length
        self.cell_height = cell_height
        pygame.init()
        self.simulator = simulator
        self.continue_drawing = 1
        # self.init_screen(simulator)
        self.screen = None
        self.entities = []

    def init_screen(self):
        self.screen = pygame.display.set_mode((self.height, self.width))
        self.entities = self.simulator.entities
        self.screen.fill(WHITE)
        pygame.display.flip()

    def create_graphic_roads(self, start, first_point=Point(200, 500)):
        stack = [(start, first_point)]
        visited = set()
        roads = []
        while stack:
            entity, pos = stack.pop()
            res = copy(pos)
            if entity not in visited:
                successors = entity.successors.values()
                predecessors = entity.predecessors.values()
                if type(entity) is Road:
                    print(entity.orientation.value)
                    res = pos.rotate_point(entity.orientation,
                                           Point(pos.x + (entity.length + 1) * self.cell_length, pos.y))
                    roads.append(GraphicRoad(pos, res, entity.nodes))
                visited.add(entity)
                next_entities = [(r, res) for r in set(successors) - visited]
                next_entities.extend([(r, pos) for r in set(predecessors) - visited])
                stack.extend(next_entities)

        return roads

    def draw(self):
        graphic_roads = self.create_graphic_roads(self.entities[0])
        for graphic_road in graphic_roads:
            graphic_road.create_sprites()
        while self.continue_drawing:
            self.simulator.tick()
            for graphic_road in graphic_roads:
                graphic_road.update()
                graphic_road.draw(self.screen)
            time.sleep(1)
            pygame.display.flip()
            self.screen.fill(WHITE)
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.continue_drawing = 0
