from copy import copy

import pygame
from pygame.locals import *

from shared import Orientation
from simulator import Exit, Entry, RightPriorityJunction
from simulator.road import Road
from visualizer.junction import GraphicJunction
from visualizer.my_sprite import CarSprite
from visualizer.point import Point
from visualizer.road import GraphicRoad

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
        self.screen = None
        self.entities = []

    def init_screen(self):
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.entities = self.simulator.entities
        self.screen.fill(WHITE)
        pygame.display.flip()

    def create_graphic_roads(self, start, first_point=Point(500, 300)):
        stack = [(start, first_point, True)]
        visited = set()
        roads = []
        nodes = []
        while stack:
            entity, pos, forward = stack.pop()
            res = copy(pos)
            if entity not in visited:
                successors = entity.successors.items()
                predecessors = entity.predecessors.items()
                if type(entity) is Road:
                    direction_pred, predecessor = next(iter(entity.predecessors.items()))
                    direction_succ, successor = next(iter(entity.successors.items()))
                    shift = 1
                    if type(predecessor) is RightPriorityJunction:
                        if entity.orientation == Orientation.NORTH or entity.orientation == Orientation.SOUTH:
                            shift = predecessor.size_north_south - 1
                            pos = pos - Point(0, shift * self.cell_length)
                        elif entity.orientation == Orientation.WEST or entity.orientation == Orientation.EAST:
                            shift = predecessor.size_east_west
                            # pos = pos - Point(shift * self.cell_length, 0)
                    res = pos.rotate_point(entity.orientation,
                                           Point(pos.x + (entity.length + 1) * self.cell_length, pos.y))
                    if not forward:
                        if type(successor) is RightPriorityJunction:
                            if entity.orientation == Orientation.NORTH or entity.orientation == Orientation.SOUTH:
                                shift = successor.size_north_south - 1
                                pos = pos + Point(0, shift * self.cell_length)
                            elif entity.orientation == Orientation.WEST or entity.orientation == Orientation.EAST:
                                shift = successor.size_east_west
                        res = pos.rotate_point(entity.orientation + 180,
                                               Point(pos.x + (entity.length + shift) * self.cell_length, pos.y))
                        pos, res = res, pos
                    roads.append(GraphicRoad(pos, res, entity, self.cell_length, self.cell_height))
                else:
                    roads.append(GraphicJunction(pos, entity, self.cell_length, self.cell_height))

                visited.add(entity)
                next_entities = [(r, pos, False) for r in set(entity.predecessors.values()) - visited]
                next_entities.extend([(r, res, True) for r in set(entity.successors.values()) - visited])
                stack.extend(next_entities)
        return roads

    def draw(self):
        graphic_roads = self.create_graphic_roads(self.simulator.entities[0])
        # node_positions = nodes
        for graphic_road in graphic_roads:
            graphic_road.create_sprites()
            # node_positions.append([graphic_roads, graphic_road.node_pos])
        clock = pygame.time.Clock()
        car_group = pygame.sprite.RenderClear()
        accumulator = 0
        car_updates = 0
        while self.continue_drawing:
            tick = clock.tick()
            accumulator += tick
            car_updates += tick
            for graphic_road in graphic_roads:
                graphic_road.draw(self.screen)
            if car_updates >= 30:
                car_group.update(tick)
                car_updates = 0
            car_group.draw(self.screen)
            if accumulator > 1000:
                self.simulator.tick()
                accumulator = 0
                for graphic_road in graphic_roads:
                    for node, pos in graphic_road.node_pos:
                        if node.current_car and type(graphic_road.entity) is not Exit and type(
                                graphic_road.entity) is not Entry:
                            sprite = next(iter(s for s in car_group.sprites() if s.car == node.current_car), None)
                            if sprite:
                                sprite.interpolate(pos)
                                # sprite.rotate(-graphic_road.angle)
                            else:
                                car_group.add(CarSprite(pos, node.current_car, 30, 20, -graphic_road.angle))
                        elif node.current_car and type(graphic_road.entity) is Exit:
                            sprite = next(iter(s for s in car_group.sprites() if s.car == node.current_car), None)
                            if sprite:
                                car_group.remove(sprite)
            pygame.display.flip()
            self.screen.fill(WHITE)
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.continue_drawing = 0

    # def interpolate(self, start, end, time_max, tick):
