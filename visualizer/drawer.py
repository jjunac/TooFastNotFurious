import time
from math import pi

import pygame
from pygame.locals import *

from simulator import *
from visualizer.road import GraphicRoad, rotate_point, CarSprite, MySprite

HEIGHT = 7
WIDTH = 12

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Drawing:

    def __init__(self, simulator):
        self.height = 30
        self.cell_length = 30
        pygame.init()
        self.simulator = simulator
        self.continue_drawing = 1
        self.screen = pygame.display.set_mode((1600, 900))
        self.nodes = simulator.nodes
        self.screen.fill(WHITE)
        pygame.display.flip()

    def generate_road_and_draw(self):
        entry_nodes = [n for n in self.nodes if type(n) is EntryNode]
        visited, roads = Drawing.depth_first_search(entry_nodes)
        self.create_graphic_roads(roads)
        return roads

    def create_graphic_roads(self, roads):
        point = (500, 500)
        nodes = {}
        graphic_roads = []
        for road in roads:
            orientation = road["road"][0].orientation
            angle = orientation * pi / 180
            road_length = len(road["road"])
            if road["entry"] in nodes:
                point = nodes[road["entry"]]

            elif road["exit"] in nodes:
                point = nodes[road["exit"]]
                angle = angle + pi
                xa, ya = rotate_point(angle, (point[0] + road_length * self.cell_length + self.cell_length, point[1]),
                                      point)
                graphic_road = GraphicRoad(xa, ya, point[0], point[1], road["road"], self.cell_length, self.height)
                nodes[road["entry"]] = (xa, ya)
                graphic_roads.append(graphic_road)
                continue
            xa, ya = rotate_point(angle, (point[0] + road_length * self.cell_length + self.cell_length, point[1]),
                                  point)
            nodes[road["exit"]] = (int(xa), int(ya))
            graphic_road = GraphicRoad(point[0], point[1], xa, ya, road["road"], self.cell_length, self.height)
            graphic_roads.append(graphic_road)
        return graphic_roads, nodes

    @staticmethod
    def depth_first_search(start):
        visited, stack = set(), start
        roads = []
        road = {"entry": None, "road": [], "exit": None}
        junctions = []
        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                if type(vertex) is RoadNode:
                    visited.add(vertex)
                    road["road"].append(vertex)
                else:
                    road["exit"] = vertex
                    if len(junctions) > 0:
                        road["entry"] = junctions[-1]
                        if len(set(junctions[-1].successors) - visited) == 0:
                            junctions.pop()
                    roads.append(road)
                    road = {"entry": None, "road": [], "exit": None}
                    if type(vertex) is not ExitNode:
                        junctions.append(vertex)
                stack.extend(set(vertex.successors) - visited)

        return visited, [r for r in roads if len(r["road"]) != 0]

    @staticmethod
    def get_road_orientation(road):
        return road["road"].orientation

    def draw(self):
        roads = self.generate_road_and_draw()
        graphic_roads, nodes = self.create_graphic_roads(roads)
        while self.continue_drawing:
            self.simulator.tick()
            for graphic_road in graphic_roads:
                graphic_road.update()
                graphic_road.draw(self.screen)
            for k, v in nodes.items():
                if type(k) is not ExitNode and type(k) is not EntryNode:
                    surface = pygame.Surface((self.cell_length, self.height))
                    surface.fill((29, 17, 17))
                    my_sprite = MySprite(v[0], v[1], self.cell_length, self.height, image=surface)
                    self.screen.blit(my_sprite.image, my_sprite.rect)
                    car = k.current_car
                    if car:
                        car_orientation = k.successors[car.get_way_index()].orientation
                        print(car_orientation)
                        sprite = CarSprite(v[0], v[1], self.cell_length, int(2 * self.height / 3),
                                           angle=-car_orientation)
                        self.screen.blit(sprite.image, sprite.rect)
            time.sleep(1)
            pygame.display.flip()
            self.screen.fill(WHITE)
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.continue_drawing = 0
