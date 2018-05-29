import unittest

from engine.road import Road
from engine.state import State


class TestRoad(unittest.TestCase):

    def test_a_car_should_go_forward_when_it_is_alone(self):
        r = Road(10)
        for c in r.cells:
            self.assertEqual(State.EMPTY, c)
        r.cells[0] = State.CAR
        for i in range(10):
            # Empty before the car
            for j in range(i):
                self.assertEqual(State.EMPTY, r.cells[j])
            # Check if the car is at the right place
            self.assertEqual(State.CAR, r.cells[i])
            # Empty after the car
            for j in range(i+1, r.length):
                self.assertEqual(State.EMPTY, r.cells[j])

            r.tick()


    def test_a_car_should_stop_when_there_is_a_car_ahead(self):
        r = Road(10)
        for c in r.cells:
            self.assertEqual(State.EMPTY, c)
        for i in range(4, 10):
            r.cells[i] = State.CAR
        r.cells[1] = State.CAR

        r.tick()
        self.assertEqual(State.EMPTY, r.cells[1])
        self.assertEqual(State.CAR, r.cells[2])
        self.assertEqual(State.EMPTY, r.cells[3])

        r.tick()
        self.assertEqual(State.EMPTY, r.cells[2])
        self.assertEqual(State.CAR, r.cells[3])
        self.assertEqual(State.CAR, r.cells[4])

        r.tick()
        self.assertEqual(State.EMPTY, r.cells[2])
        self.assertEqual(State.CAR, r.cells[3])
        self.assertEqual(State.CAR, r.cells[4])

    def test_a_car_should_wait_before_go_forward_when_there_is_a_car_ahead(self):
        r = Road(3)
        r.cells[0] = State.CAR
        r.cells[1] = State.CAR
        r.cells[2] = State.CAR

        r.tick()
        self.assertEqual(State.CAR, r.cells[0])
        self.assertEqual(State.CAR, r.cells[1])
        self.assertEqual(State.EMPTY, r.cells[2])

        r.tick()
        self.assertEqual(State.CAR, r.cells[0])
        self.assertEqual(State.EMPTY, r.cells[1])
        self.assertEqual(State.CAR, r.cells[2])

        r.tick()
        self.assertEqual(State.EMPTY, r.cells[0])
        self.assertEqual(State.CAR, r.cells[1])
        self.assertEqual(State.EMPTY, r.cells[2])

        r.tick()
        self.assertEqual(State.EMPTY, r.cells[0])
        self.assertEqual(State.EMPTY, r.cells[1])
        self.assertEqual(State.CAR, r.cells[2])

        r.tick()
        self.assertEqual(State.EMPTY, r.cells[0])
        self.assertEqual(State.EMPTY, r.cells[1])
        self.assertEqual(State.EMPTY, r.cells[2])
