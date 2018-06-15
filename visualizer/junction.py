import pygame

from shared import Orientation
from simulator.stop_junction import StopJunction
from simulator.traffic_light_junction import TrafficLightJunction
from visualizer.my_sprite import MySprite, StopSprite
from visualizer.point import Point
from visualizer.road import GraphicEntity


class GraphicJunction(GraphicEntity):

    def __init__(self, position, junction, cell_length=30, cell_height=30, forward=False, previous_road=None):
        super().__init__(position, junction, cell_length, cell_height)
        if self.entity.size_east_west > 1 or self.entity.size_north_south > 1:
            first = Orientation.NORTH if forward else Orientation.SOUTH
            second = Orientation.WEST if forward else Orientation.EAST
            if previous_road.orientation == first and self.entity.size_north_south - previous_road.n_of_ways > 0:
                self.position = self.position - (
                    (self.entity.size_north_south - 1 * previous_road.n_of_ways) * cell_height, 0)
            elif previous_road.orientation == second and self.entity.size_east_west - previous_road.n_of_ways > 0:
                self.position = self.position - (
                    1 * cell_length, -(self.entity.size_east_west - 1 * previous_road.n_of_ways) * cell_height)
            elif previous_road.orientation == Orientation.SOUTH:
                self.position = self.position + (0, max((self.entity.size_east_west - 1), 1) * cell_height)
            elif previous_road.orientation == second:
                self.position = self.position - (max((self.entity.size_north_south - 1), 1) * cell_height, 0)
        for i in range(len(self.entity.nodes)):
            for j in range(len(self.entity.nodes[i])):
                point = self.position + Point(j * self.cell_length, -i * self.cell_height)
                self.node_pos.append((self.entity.nodes[i][j], point))

    def create_sprites(self):
        for cell, pos in self.node_pos:
            surface = pygame.Surface((self.cell_length, self.cell_height))
            surface.fill((29, 17, 17))
            self.group.add(MySprite(pos, self.cell_length, self.cell_height, image=surface))


def draw(self, surface):
    self.group.draw(surface)


class GraphicStopJunction(GraphicJunction):
    def __init__(self, position: Point, junction, cell_length=30, cell_height=30, forward=False, previous_road=None):
        super().__init__(position, junction, cell_length, cell_height, forward, previous_road)

    def create_sprites(self):
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


class GraphicTrafficLightJunction(GraphicJunction):
    def __init__(self, position: Point, junction, cell_length=30, cell_height=30, forward=False, previous_road=None):
        super().__init__(position, junction, cell_length, cell_height, forward, previous_road)
        self.lights = [[], []]

    def create_sprites(self):
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

    def update(self, car_group):
        super(GraphicTrafficLightJunction, self).update(car_group)
        lights = self.get_traffic_light_state()
        for i in range(len(lights)):
            for sprite in self.lights[i]:
                surfarray = pygame.PixelArray(sprite.image)
                if lights[i]:
                    surfarray.replace((255, 0, 0), (0, 255, 0))
                else:
                    surfarray.replace((0, 255, 0), (255, 0, 0))

    def get_traffic_light_state(self):
        if self.entity.counter < self.entity.state1_timer:
            state1 = True
            state2 = False
        elif self.entity.counter < self.entity.state1_timer + self.entity.interval:
            state1 = False
            state2 = False
        elif self.entity.counter < self.entity.state1_timer + self.entity.interval + self.entity.state2_timer:
            state1 = False
            state2 = True
        else:
            state2 = False
            state1 = False
        return [state1, state2]
