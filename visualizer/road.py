from math import atan2

from pygame.sprite import RenderClear

from visualizer.my_sprite import RoadSprite, CarSprite
from visualizer.point import Point, to_degrees


class GraphicEntity:

    def __init__(self, position, entity, cell_length=30, cell_height=30):
        super().__init__()
        self.position = position
        self.group = RenderClear()
        self.entity = entity
        self.cell_length = cell_length
        self.cell_height = cell_height
        self.node_pos = []
        self.angle = 0

    def create_sprites(self):
        for i in self.entity.nodes:
            for n in i:
                self.node_pos.append((n, self.position))

    def draw(self, surface):
        self.group.draw(surface)

    def update(self, car_group):
        for node, pos in self.node_pos:
            if node.current_car:
                sprite = next(iter(s for s in car_group.sprites() if s.car == node.current_car), None)
                if sprite:
                    sprite.interpolate(pos)
                else:
                    car_group.add(CarSprite(pos, node.current_car, 30, 20, -self.angle))


class GraphicExit(GraphicEntity):

    def __init__(self, position, entity, cell_length=30, cell_height=30):
        super().__init__(position, entity, cell_length, cell_height)

    def update(self, car_group):
        for node, pos in self.node_pos:
            sprite = next(iter(s for s in car_group.sprites() if s.car == node.current_car), None)
            if sprite:
                car_group.remove(sprite)


class GraphicRoad(GraphicEntity):

    def __init__(self, position, end, road, cell_length=30, cell_height=30, road_number=0):
        super().__init__(position, road, cell_length, cell_height)
        self.end = end
        self.road_number = road_number
        self.angle = to_degrees(atan2(self.end.y - self.position.y, self.end.x - self.position.x))
        self.sprite_start = self.position.rotate_point(self.angle,
                                                       Point(self.position.x + self.cell_length, self.position.y))
        self.sprite_end = end.rotate_point(self.angle, Point(self.end.x - self.cell_length, self.end.y))
        tmp = self.sprite_start.rotate_point(self.angle,
                                             Point(self.sprite_start.x + self.cell_length, self.sprite_start.y))
        self.pos_i = tmp - self.sprite_start

    def create_sprites(self):
        for k in range(self.entity.n_of_ways):
            if self.angle == 180 or self.angle == -90:
                p = self.sprite_start.rotate_point(self.angle,
                                                   Point(self.sprite_start.x,
                                                         self.sprite_start.y + k * self.cell_height))
            else:
                p = self.sprite_start.rotate_point(self.angle,
                                                   Point(self.sprite_start.x,
                                                         self.sprite_start.y - k * self.cell_height))
            x = p.x
            y = p.y
            i = 0
            while i < len(self.entity.nodes[k]):
                pos = Point(x + self.pos_i.x * i, y + self.pos_i.y * i)
                self.node_pos.append((self.entity.nodes[k][i], pos))
                road_portion = RoadSprite(pos, self.cell_length, self.cell_height, -self.angle)
                self.group.add(road_portion)
                i += 1
