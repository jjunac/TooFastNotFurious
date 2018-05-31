from math import pi

import pygame
from pygame.locals import *

from simulator import EntryNode, RoadNode
from visualizer.road import GraphicRoad, rotate_point

HEIGHT = 7
WIDTH = 12

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Drawing:

    def __init__(self, nodes):
        pygame.init()

        self.continue_drawing = 1
        self.fenetre = pygame.display.set_mode((1600, 900))
        self.nodes = nodes
        self.fenetre.fill(WHITE)
        pygame.display.flip()

    def drawRoad(self):
        entry_nodes = [n for n in self.nodes if type(n) is EntryNode]
        visited, roads = Drawing.depth_first_search(entry_nodes)
        point = (500, 500)
        cell_length = 30
        height = 30
        nodes = {}
        for road in roads:
            orientation = road["road"][0].orientation
            angle = orientation * pi / 180

            if road["entry"] in nodes:
                point = nodes[road["entry"]]
            if road["exit"] in nodes:
                point = nodes[road["exit"]]
                angle = angle + pi
            pygame.draw.circle(self.fenetre, (0, 255, 0), point, 10)
            road_length = len(road["road"])

            xa, ya = rotate_point(angle, (point[0] + road_length * cell_length, point[1]), point)
            nodes[road["exit"]] = (int(xa), int(ya))
            graphic_road = GraphicRoad(point[0], point[1], xa, ya, None, cell_length, height)
            graphic_road.draw(self.fenetre)
            pygame.draw.circle(self.fenetre, (0, 255, 0), (int(xa), int(ya)), 10)

    @staticmethod
    def depth_first_search(start):
        visited, stack = set(), start
        roads = []
        road = {"entry": None, "road": [], "exit": None}
        while stack:
            vertex = stack.pop()
            if vertex not in visited:

                if type(vertex) is RoadNode:
                    visited.add(vertex)
                    road["road"].append(vertex)
                else:
                    road["exit"] = vertex
                    roads.append(road)
                    road = {"entry": vertex, "road": [], "exit": None}
                stack.extend(set(vertex.successors) - visited)

        return visited, [r for r in roads if len(r["road"]) != 0]

    def draw(self):

        self.drawRoad()
        pygame.display.flip()
        while self.continue_drawing:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.continue_drawing = 0
