import pygame
from pygame.sprite import RenderClear

from shared import Orientation
from simulator.junction import Junction
from simulator.right_priority_junction import RightPriorityJunction
from simulator.stop_junction import StopJunction
from simulator.traffic_light_junction import TrafficLightJunction
from visualizer.my_sprite import MySprite, StopSprite
from visualizer.point import Point


class GraphicJunction:

    def __init__(self, position: Point, junction, cell_length=30, cell_height=30, previous_road=None):
        super().__init__()
        self.position = position
        self.group = RenderClear()
        self.entity = junction
        self.cell_length = cell_length
        self.cell_height = cell_height
        self.angle = 0
        self.lights = [[], []]
        self.node_pos = []
        if isinstance(self.entity, Junction):
            surface = pygame.Surface((self.cell_length, self.cell_height))
            surface.fill((29, 17, 17))
            if self.entity.size_east_west > 1 or self.entity.size_north_south > 1:
                if previous_road.orientation == Orientation.NORTH and self.entity.size_north_south - previous_road.n_of_ways > 0:
                    self.position = self.position - ((self.entity.size_north_south - 1) * cell_height, 0)
                elif previous_road.orientation == Orientation.WEST and self.entity.size_east_west - previous_road.n_of_ways > 0:
                    self.position = self.position - (0, (self.entity.size_east_west - 1) * cell_height)
                elif previous_road.orientation == Orientation.SOUTH:
                    self.position = self.position + (0, max((self.entity.size_east_west - 1), 1) * cell_height)
                elif previous_road.orientation == Orientation.WEST:
                    self.position = self.position - (max((self.entity.size_east_west - 1), 1) * cell_height, 0)
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
            nodes_orientations = [i for n in self.entity.get_end_of_predecessor(self.entity.stop_orientation) for i in
                                  n.successors]
            for cell, pos in self.node_pos:
                if cell not in nodes_orientations:
                    surface = pygame.Surface((self.cell_length, self.cell_height))
                    surface.fill((29, 17, 17))
                    self.group.add(MySprite(pos, self.cell_length, self.cell_height, image=surface))
                else:
                    self.group.add(StopSprite(pos, self.cell_length, self.cell_height, -self.entity.stop_orientation))
        elif type(self.entity) is TrafficLightJunction:
            self.entity: TrafficLightJunction
            nodes_orientations = [(k, o) for o in self.entity.state1_orientations + self.entity.state2_orientations
                                  for n in self.entity.get_end_of_predecessor(o) for k in n.successors]
            nodes = [k[0] for k in nodes_orientations]
            for cell, pos in self.node_pos:
                if cell in nodes:
                    orientations = [k[1] for k in nodes_orientations if k[0] == cell]
                    i = 0
                    for o in orientations:
                        point = pos.rotate_point(o, pos + (self.cell_length, -self.cell_height))
                        surface = pygame.Surface((self.cell_length, self.cell_height), pygame.SRCALPHA)
                        pygame.draw.circle(surface, (255, 0, 0),
                                           (round(self.cell_length / 2), round(self.cell_height / 2)),
                                           round(self.cell_length / 2))
                        sprite = MySprite(point, round(self.cell_length / 2), round(self.cell_height / 2),
                                          image=surface)
                        self.group.add(sprite)
                        self.lights[i].append(sprite)
                        i += 1

                surface = pygame.Surface((self.cell_length, self.cell_height))
                surface.fill((29, 17, 17))
                self.group.add(MySprite(pos, self.cell_length, self.cell_height, image=surface))

    def draw(self, surface):
        self.group.draw(surface)
