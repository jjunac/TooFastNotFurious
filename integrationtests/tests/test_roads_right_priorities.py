from modeler import *
from shared import Orientation
import unittest
import random


class TestRoadRightPriorities(unittest.TestCase):
    def test_non_priority_cars_should_not_pass_when_there_is_a_continuous_car_flow_at_their_right(self):
        s = new_simulation()

        entry1 = entry_node().with_rate(1)
        s.add_node(entry1)
        entry2 = entry_node().with_rate(1)
        s.add_node(entry2)
        exit1 = exit_node()
        s.add_node(exit1)
        junction = right_priority_junction()
        s.add_node(junction)

        s.add_road(entry1.connect(Orientation.NORTH).to(junction).with_length(2))
        s.add_road(entry2.connect(Orientation.WEST).to(junction).with_length(1))
        s.add_road(junction.connect(Orientation.SOUTH).to(exit1).with_length(1))

        s.add_path(entry1.go_through(junction, exit1).with_proportion(100))
        s.add_path(entry2.go_through(junction, exit1).with_proportion(100))

        s.run_for(500)
        self.assertFalse(s.node_conversion[entry1] in s.node_conversion[exit1].departure_counter)


if __name__ == '__main__':
    unittest.main()