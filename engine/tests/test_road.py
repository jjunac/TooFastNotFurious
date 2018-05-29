import unittest

from engine.road import Road


class TestRoad(unittest.TestCase):

    def test_a_car_should_go_forward_when_it_is_alone(self):
        r = Road(10)
        for _ in range(20):
            r.tick()
            print(r.cells)