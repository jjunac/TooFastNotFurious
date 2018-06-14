import pygame
from pygame.locals import *

from simulator import Exit
from simulator.junction import Junction
from simulator.road import Road
from simulator.roundabout import Roundabout
from simulator.stop_junction import StopJunction
from simulator.traffic_light_junction import TrafficLightJunction
from visualizer.junction import GraphicJunction, GraphicTrafficLightJunction, GraphicStopJunction
from visualizer.point import Point
from visualizer.road import GraphicRoad, GraphicExit

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
            if entity not in visited and type(entity) is not Roundabout:
                predecessors = entity.predecessors.values()
                successors = entity.successors.values()
                if isinstance(entity, Junction):
                    junction = create_graphic_entity(entity, forward, pos, self.cell_length, self.cell_height,
                                                     roads[-1].entity)
                    roads.append(junction)
                    next_entities = self.get_correct_road_positions(entity, junction, visited)
                    stack.extend(next_entities)
                    visited.add(entity)
                    continue
                graphic_entity, pos, res = create_graphic_entity(entity, forward, pos, self.cell_length,
                                                                 self.cell_height)
                if graphic_entity:
                    roads.append(graphic_entity)
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

    def draw(self):
        graphic_entities = self.create_graphic_roads(self.simulator.entities[0])
        graphic_entities.sort(key=lambda r: str(type(r)))
        for graphic_road in graphic_entities:
            graphic_road.create_sprites()
        clock = pygame.time.Clock()
        car_group = pygame.sprite.RenderClear()
        accumulator = 0
        car_updates = 0
        while self.continue_drawing:
            tick = clock.tick()
            accumulator += tick
            car_updates += tick
            for graphic_road in graphic_entities:
                graphic_road.draw(self.screen)
            if car_updates >= 20:
                car_group.update(tick)
                car_updates = 0
            car_group.draw(self.screen)
            if accumulator > 1000:
                self.simulator.tick()
                accumulator = 0
                for road in graphic_entities:
                    road.update(car_group)
            pygame.display.flip()
            self.screen.fill(WHITE)
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.continue_drawing = 0


def create_graphic_entity(entity, forward, pos, cell_length, cell_height, previous_road=None):
    if type(entity) is Road:
        res = pos.rotate_point(entity.orientation,
                               Point(pos.x + (entity.length + 1) * cell_length, pos.y))
        if not forward:
            res = pos.rotate_point(entity.orientation + 180,
                                   Point(pos.x + (entity.length + 1) * cell_length, pos.y))
            pos, res = res, pos
        return GraphicRoad(pos, res, entity, cell_length, cell_height), pos, res
    elif isinstance(entity, Junction):
        if type(entity) is StopJunction:
            return GraphicStopJunction(pos, entity, cell_length, cell_height, forward, previous_road)
        elif type(entity) is TrafficLightJunction:
            return GraphicTrafficLightJunction(pos, entity, cell_length, cell_height, forward, previous_road)
        else:
            return GraphicJunction(pos, entity, cell_length, cell_height, forward, previous_road)
    elif type(entity) is Exit:
        return GraphicExit(pos, entity, cell_length, cell_height), pos, pos
    else:
        return None, pos, pos
