import pygame
from pygame.sprite import RenderClear

from simulator import RightPriorityJunction
from simulator.junction import Junction
from simulator.stop_junction import StopJunction
from visualizer.my_sprite import MySprite, StopSprite
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
        if type(self.entity) is Junction:
            surface = pygame.Surface((self.cell_length, self.cell_height))
            surface.fill((29, 17, 17))
            for i in range(len(self.entity.nodes)):
                for j in range(len(self.entity.nodes[i])):
                    point = self.position + Point(j * self.cell_length, -i * self.cell_height)
                    self.node_pos.append((self.entity.nodes[i][j], point))
        else:
            for i in self.entity.nodes:
                for n in i:
                    self.node_pos.append((n, self.position))

    def create_sprites(self):
        if type(self.entity) is RightPriorityJunction:
            for cell, pos in self.node_pos:
                surface = pygame.Surface((self.cell_length, self.cell_height))
                surface.fill((29, 17, 17))
                self.group.add(MySprite(pos, self.cell_length, self.cell_height, image=surface))
        elif type(self.entity) is StopJunction:
            self.entity: StopJunction
            nodes = self.entity.get_end_of_predecessor(self.entity.stop_orientation)[0].successors
            for cell, pos in self.node_pos:
                if cell not in nodes:
                    surface = pygame.Surface((self.cell_length, self.cell_height))
                    surface.fill((29, 17, 17))
                    self.group.add(MySprite(pos, self.cell_length, self.cell_height, image=surface))
                else:
                    self.group.add(StopSprite(pos, self.cell_length, self.cell_height, -self.entity.stop_orientation))

    def draw(self, surface):
        self.group.draw(surface)
