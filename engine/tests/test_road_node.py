import unittest

from engine.road_node import RoadNode


class MyTestCase(unittest.TestCase):

    def build_road(self, length):
        res = [RoadNode()]
        for i in range(length-1):
            res.append(RoadNode())
            res[-2].successors.append(res[-1])
            res[-1].predecessors.append(res[-2])
        return res


    def compute_next(self, road):
        for n in road:
            n.compute_next()

    def apply_next(self, road):
        for n in road:
            n.apply_next()


    def test_a_car_should_go_forward_when_it_is_alone(self):
        road = self.build_road(10)
        for n in road:
            self.assertEqual(False, n.is_car_present)
        road[0].is_car_present = True
        for i in range(10):
            # Empty before the car
            for j in range(i):
                self.assertEqual(False, road[j].is_car_present)
            # Check if the car is at the right place
            self.assertEqual(True, road[i].is_car_present)
            # Empty after the car
            for j in range(i+1, len(road)):
                self.assertEqual(False, road[j].is_car_present)
            self.compute_next(road)
            self.apply_next(road)


    def test_a_car_should_stop_when_there_is_a_car_ahead(self):
        road = self.build_road(10)
        for c in road:
            self.assertFalse(False, c.is_car_present)
        for i in range(4, 10):
            road[i].is_car_present = True
        road[1].is_car_present = True

        self.compute_next(road)
        self.apply_next(road)
        self.assertEqual(False, road[1].is_car_present)
        self.assertEqual(True, road[2].is_car_present)
        self.assertEqual(False, road[3].is_car_present)

        self.compute_next(road)
        self.apply_next(road)
        self.assertEqual(False, road[2].is_car_present)
        self.assertEqual(True, road[3].is_car_present)
        self.assertEqual(True, road[4].is_car_present)

        self.compute_next(road)
        self.apply_next(road)
        self.assertEqual(False, road[2].is_car_present)
        self.assertEqual(True, road[3].is_car_present)
        self.assertEqual(True, road[4].is_car_present)

    def test_a_car_should_wait_before_go_forward_when_there_is_a_car_ahead(self):
        road = self.build_road(3)
        road[0].is_car_present = True
        road[1].is_car_present = True
        road[2].is_car_present = True

        self.compute_next(road)
        self.apply_next(road)
        self.assertEqual(True, road[0].is_car_present)
        self.assertEqual(True, road[1].is_car_present)
        self.assertEqual(False, road[2].is_car_present)

        self.compute_next(road)
        self.apply_next(road)
        self.assertEqual(True, road[0].is_car_present)
        self.assertEqual(False, road[1].is_car_present)
        self.assertEqual(True, road[2].is_car_present)

        self.compute_next(road)
        self.apply_next(road)
        self.assertEqual(False, road[0].is_car_present)
        self.assertEqual(True, road[1].is_car_present)
        self.assertEqual(False, road[2].is_car_present)

        self.compute_next(road)
        self.apply_next(road)
        self.assertEqual(False, road[0].is_car_present)
        self.assertEqual(False, road[1].is_car_present)
        self.assertEqual(True, road[2].is_car_present)

        self.compute_next(road)
        self.apply_next(road)
        self.assertEqual(False, road[0].is_car_present)
        self.assertEqual(False, road[1].is_car_present)
        self.assertEqual(False, road[2].is_car_present)


if __name__ == '__main__':
    unittest.main()