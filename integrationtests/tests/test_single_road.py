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

        s.add_road(e1.connect(Orientation.NORTH).to(e2).with_length(18))

        s.add_path(e1.to(e2).with_proportion(100))

        random.seed(0)
        # With seed 0 and a rate of 0.2, 38 cars are generated in 200 tick, plus 20 tick to reach the end
        # Code used to compute:
        """
        res = 0
        random.seed(0)
        for _ in range(200):
            if random.random() <= 0.2:
                res += 1
                random.random()
                random.choice([0])
        """
        s.run_for(220)
        self.assertEqual(38, s.entity_conversion[e2].outflow)

    def test_double_road(self):
        s = new_simulation()

        e1 = entry_node().with_rate(0.2)
        s.add_node(e1)
        e2 = exit_node()
        s.add_node(e2)

        s.add_road(e1.connect(Orientation.NORTH).to(e2).with_length(18).with_n_ways(2))

        s.add_path(e1.to(e2).with_proportion(100))

        random.seed(0)
        # With seed 0, 39 cars are generated in 200 tick, plus 20 tick to reach the end
        s.run_for(220)
        self.assertEqual(39, s.entity_conversion[e2].outflow)

if __name__ == '__main__':
    unittest.main()