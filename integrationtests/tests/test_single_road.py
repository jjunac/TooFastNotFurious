from modeler import *
from shared import Orientation
import unittest
import random


class TestSingleRoad(unittest.TestCase):
    def test_single_road(self):
        s = new_simulation()

        e1 = entry_node().with_rate(0.2)
        s.add_node(e1)
        e2 = exit_node()
        s.add_node(e2)

        s.add_road(e1.connect(Orientation.NORTH).to(e2).with_length(20))

        s.add_path(e1.to(e2).with_proportion(100))

        random.seed(0)
        # With seed 0, 32 cars are generated in 200 tick, plus 21 tick to reach the end
        s.run_for(221)
        self.assertEqual(32, s.entity_conversion[e2].outflow)


if __name__ == '__main__':
    unittest.main()