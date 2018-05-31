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

        self.continuer = 1
        self.fenetre = pygame.display.set_mode((1600, 900))
        self.nodes = nodes
        self.fenetre.fill(WHITE)
        pygame.display.flip()

    def drawRoad(self):
        entry_nodes = [n for n in self.nodes if type(n) is EntryNode]
        entry = entry_nodes[0]
        visited, roads = Drawing.depth_first_search(entry)
        point = (500, 500)
        cell_length = 30
        height = 30
        for road in roads:
            print(point)
            pygame.draw.circle(self.fenetre, (255, 0, 0), point, 10)
            road_length = len(road["road"])
            orientation = road["road"][0].orientation
            angle = orientation * pi / 180
            xa, ya = rotate_point(angle, (point[0] + road_length * cell_length, point[1]), point)
            graphic_road = GraphicRoad(point[0], point[1], xa, ya, None, cell_length, height)
            graphic_road.draw(self.fenetre)
            point = (int(xa), int(ya))
            pygame.draw.circle(self.fenetre, (0, 255, 0), point, 10)

    @staticmethod
    def depth_first_search(start):
        visited, stack = set(), [start]
        roads = []
        road = {"entry": None, "road": [], "exit": None}

        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                if type(vertex) is RoadNode:
                    road["road"].append(vertex)
                else:
                    road["exit"] = vertex
                    roads.append(road)
                    road = {"entry": vertex, "road": [], "exit": None}
                visited.add(vertex)
                stack.extend(set(vertex.successors) - visited)
        roads.pop(0)
        return visited, roads

    def draw(self):
        # r = GraphicRoad(100, 100, 600, 100, None, cell_length=50, height=50)
        # r2 = GraphicRoad(400, 0, 400, 500, None, cell_length=50, height=50)
        # r.draw(self.fenetre)
        # # r2.draw(self.fenetre)
        # j = Junction(200, 500, None, length=50, height=50)
        # j1 = Junction(400, 500, None, 3, Orientation.NORTH, length=50, height=50)
        # j2 = Junction(600, 500, None, 3, Orientation.NORTH, length=50, height=50)
        # j3 = Junction(800, 500, None, 3, Orientation.EAST, length=50, height=50)
        # j4 = Junction(1000, 500, None, 3, Orientation.WEST, length=50, height=50)
        # j.draw(self.fenetre)
        # j1.draw(self.fenetre)
        # # j2.draw(self.fenetre)
        # # j3.draw(self.fenetre)
        # # j4.draw(self.fenetre)
        #
        # pygame.draw.circle(self.fenetre, (255, 0, 0), (100, 100), 10)
        # pygame.draw.circle(self.fenetre, (255, 0, 0), (0, 0), 10)
        # pygame.draw.circle(self.fenetre, (255, 0, 0), (200, 400), 10)
        # # pygame.draw.circle(self.fenetre, (255, 0, 0), (400, 500), 10)
        # pygame.draw.circle(self.fenetre, (255, 0, 0), (600, 500), 10)
        # pygame.draw.circle(self.fenetre, (255, 0, 0), (800, 500), 10)
        # pygame.draw.circle(self.fenetre, (255, 0, 0), (1000, 500), 10)
        # sprite = RoadSprite(400, 450, 50, 50, Orientation.SOUTH)
        # clear = pygame.sprite.RenderClear()
        # clear.add(sprite)
        # clear.draw(pygame.display.get_surface())
        self.drawRoad()
        pygame.display.flip()
        while self.continuer:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.continuer = 0

# if __name__ == '__main__':
#     Drawing([]).draw()
