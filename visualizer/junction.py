import pygame
from pygame.sprite import RenderClear

from simulator import RightPriorityJunction
from visualizer.my_sprite import MySprite
from visualizer.point import Point


class GraphicJunction:

    def __init__(self, position, junction, cell_length=30, cell_height=30):
        super().__init__()
        self.position = position
        self.group = RenderClear()
        self.entity = junction
        self.cell_length = cell_length
        self.cell_height = cell_height
        self.angle = 0
        self.node_pos = []

    def create_sprites(self):
        if type(self.entity) is RightPriorityJunction:
            surface = pygame.Surface((self.cell_length, self.cell_height))
            surface.fill((29, 17, 17))
            for i in range(self.entity.size_north_south):
                for j in range(self.entity.size_east_west):
                    point = self.position + Point(j * self.cell_length, -i * self.cell_height)
                    self.group.add(
                        MySprite(point, self.cell_length,
                                 self.cell_height, image=surface))
                    self.node_pos.append((self.entity.nodes[i][j], point))
        else:
            for i in self.entity.nodes:
                for n in i:
                    self.node_pos.append((n, self.position))

    def draw(self, surface):
        self.group.draw(surface)
