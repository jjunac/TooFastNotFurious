import pygame
from pygame.sprite import RenderClear

from simulator.right_priority_junction import RightPriorityJunction
from visualizer.my_sprite import MySprite


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
            self.group.add(MySprite(self.position, self.cell_length, self.cell_height, image=surface))
        self.node_pos.append((self.entity.nodes[0], self.position))

    def draw(self, surface):
        self.group.draw(surface)
