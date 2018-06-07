import unittest

from shared import Orientation
from simulator import Road, Simulator
from simulator.car import Car
from simulator.path import Path
from simulator.right_priority_junction import RightPriorityJunction
from simulator.stop_junction import StopJunction
from simulator.utils import *
from copy import deepcopy


class TestStopJunction(unittest.TestCase):

    def test_coucou(self):
        self.assertTrue(True)
