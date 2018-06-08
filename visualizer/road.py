from math import atan2

from pygame.sprite import RenderClear

from visualizer.my_sprite import RoadSprite
from visualizer.point import Point, to_degrees


class GraphicRoad:

    def __init__(self, start, end, road, cell_length=30, cell_height=30):
        super().__init__()
        self.start = start
        self.end = end
        self.group = RenderClear()
        self.entity = road
        self.cell_length = cell_length
        self.cell_height = cell_height
        self.angle = to_degrees(atan2(self.end.y - self.start.y, self.end.x - self.start.x))
        self.sprite_start = start.rotate_point(self.angle, Point(self.start.x + self.cell_length, self.start.y))
        self.sprite_end = end.rotate_point(self.angle, Point(self.end.x - self.cell_length, self.end.y))
        tmp = self.sprite_start.rotate_point(self.angle,
                                             Point(self.sprite_start.x + self.cell_length, self.sprite_start.y))
        self.pos_i = tmp - self.sprite_start
        self.node_pos = []

    def create_sprites(self):
        vector = self.end - self.sprite_start
        dist = vector.length()
        for k in range(len(self.entity.nodes)):
            p = self.sprite_start.rotate_point(self.angle,
                                               Point(self.sprite_start.x, self.sprite_start.y + k * self.cell_height))
            x = p.x
            y = p.y
            i = 0
            while i < len(self.entity.nodes[k]):
                pos = Point(x + self.pos_i.x * i, y + self.pos_i.y * i)
                self.node_pos.append((self.entity.nodes[k][i], pos))
                road_portion = RoadSprite(pos, self.cell_length, self.cell_height, -self.angle)
                self.group.add(road_portion)
                i += 1

    def update(self):
        pass

    def draw(self, surface):
        self.group.draw(surface)
