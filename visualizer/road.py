from math import atan2

import pygame

from visualizer.my_sprite import RoadSprite
from visualizer.point import Point, to_degrees


class GraphicRoad(pygame.sprite.RenderClear):

    def __init__(self, start, end, road_cells, cell_length=30, cell_height=30):
        super().__init__()
        self.start = start
        self.end = end
        self.road_cells = road_cells
        self.cell_length = cell_length
        self.cell_height = cell_height
        self.angle = to_degrees(atan2(self.end.y - self.start.y, self.end.x - self.start.x))
        self.fake_start = start.rotate_point(self.angle, Point(self.start.x + self.cell_length, self.start.y))
        tmp = self.fake_start.rotate_point(self.angle, Point(self.fake_start.x + self.cell_length, self.fake_start.y))
        self.pos_i = tmp - self.fake_start

    def create_sprites(self):
        vector = self.end - self.fake_start
        dist = vector.length()
        i = 0
        while i < int(dist / self.cell_length):
            road_portion = RoadSprite(Point(self.fake_start.x + self.pos_i.x * i, self.fake_start.y + self.pos_i.y * i),
                                      self.cell_length, self.cell_height, self.angle)
            self.add(road_portion)
            i += 1

    def update(self):
        pass
