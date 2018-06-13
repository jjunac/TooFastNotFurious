from copy import copy

import pygame
from pygame.locals import *

from simulator import Exit, Entry, RightPriorityJunction
from simulator.road import Road
from simulator.traffic_light_junction import TrafficLightJunction
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
        while stack:
            entity, pos, forward = stack.pop()
            res = copy(pos)
            if entity not in visited:
                predecessors = entity.predecessors.values()
                successors = entity.successors.values()
                if type(entity) is Road:
                    res = pos.rotate_point(entity.orientation,
                                           Point(pos.x + (entity.length + 1) * self.cell_length, pos.y))
                    if not forward:
                        res = pos.rotate_point(entity.orientation + 180,
                                               Point(pos.x + (entity.length + 1) * self.cell_length, pos.y))
                        pos, res = res, pos
                    roads.append(GraphicRoad(pos, res, entity, self.cell_length, self.cell_height))
                elif type(entity) is RightPriorityJunction:
                    junction = GraphicJunction(pos, entity, self.cell_length, self.cell_height, roads[-1].entity)
                    roads.append(junction)
                    next_entities = self.get_correct_road_positions(entity, junction, visited)
                    stack.extend(next_entities)
                    visited.add(entity)
                    continue
                else:
                    roads.append(GraphicJunction(pos, entity, self.cell_length, self.cell_height))
                visited.add(entity)
                next_entities = [(r, pos, False) for r in set(predecessors) - visited]
                next_entities.extend([(r, res, True) for r in set(successors) - visited])
                stack.extend(next_entities)
        return roads

    @staticmethod
    def get_correct_road_positions(entity, junction, visited):
        next_entities = []
        for value in entity.predecessors.values():
            end = [i for n in value.get_end(None) for i in n.successors]
            cell, pos = next(((cell, pos) for cell, pos in junction.node_pos if cell in end), None)
            if value not in visited:
                next_entities.append((value, pos, False))
        for value in entity.successors.values():
            start = [i for n in value.get_start(None) for i in n.predecessors]
            cell, pos = next(((cell, pos) for cell, pos in junction.node_pos if cell in start), None)
            if value not in visited:
                next_entities.append((value, pos, True))
        return next_entities

    def start_point(self, point, angle, iterations):
        res = []
        for k in range(iterations):
            res.append(point.rotate_point(angle, point - (0, k * self.cell_height)))
        return res

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
            if car_updates >= 20:
                car_group.update(tick)
                car_updates = 0
            car_group.draw(self.screen)
            if accumulator > 1000:
                self.simulator.tick()
                accumulator = 0
                self.tick_cars(car_group, graphic_roads)
            pygame.display.flip()
            self.screen.fill(WHITE)
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.continue_drawing = 0

    @staticmethod
    def tick_cars(car_group, entities):
        for road in entities:
            if type(road.entity) is TrafficLightJunction:
                lights = get_traffic_light_state(road)
                for i in range(len(lights)):
                    sprite = road.lights[i]
                    surfarray = pygame.PixelArray(sprite.image)
                    if lights[i]:
                        surfarray.replace((255, 0, 0), (0, 255, 0))
                    else:
                        surfarray.replace((0, 255, 0), (255, 0, 0))
            for node, pos in road.node_pos:
                if node.current_car and type(road.entity) is not Exit and type(
                        road.entity) is not Entry:
                    sprite = next(iter(s for s in car_group.sprites() if s.car == node.current_car), None)
                    if sprite:
                        sprite.interpolate(pos)
                    else:
                        car_group.add(CarSprite(pos, node.current_car, 30, 20, -road.angle))
                elif node.current_car and type(road.entity) == Exit:
                    sprite = next(iter(s for s in car_group.sprites() if s.car == node.current_car), None)
                    if sprite:
                        car_group.remove(sprite)


def get_traffic_light_state(road):
    if road.entity.counter < road.entity.state1_timer:
        state1 = True
        state2 = False
    elif road.entity.counter < road.entity.state1_timer + road.entity.interval:
        state1 = False
        state2 = False
    elif road.entity.counter < road.entity.state1_timer + road.entity.interval + road.entity.state2_timer:
        state1 = False
        state2 = True
    else:
        state2 = False
        state1 = False
    return [state1, state2]
