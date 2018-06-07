from modeler import *
from shared import Orientation
import unittest
import random

from simulator import Entry, Exit


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

        s.add_path(entry1.to(exit1).with_proportion(100))
        s.add_path(entry2.to(exit1).with_proportion(100))

        random.seed(0)

        s.build_all()

        # --- Assertions ---
        simulator = s.simulator
        number_of_car = 0
        entry_nodes = [n for e in simulator.entities if type(e) is Entry for row in e.nodes for n in row]
        exit_nodes = [n for e in simulator.entities if type(e) is Exit for row in e.nodes for n in row]

        blocked_entry_nodes = set([])

        for _ in range(1000):
            # Subtracts cars that exit this turn
            number_of_car -= len([n for n in exit_nodes if n.current_car])
            simulator.tick()
            # Adds cars that appeared this turn
            entry_node_with_car = set([n for n in entry_nodes if n.current_car])
            number_of_car += len(entry_node_with_car - blocked_entry_nodes)
            blocked_entry_nodes = entry_node_with_car
            actual_number_of_car = len([n for e in simulator.entities for row in e.nodes for n in row if n.current_car])
            self.assertEqual(number_of_car, actual_number_of_car)

        self.assertFalse(s.entity_conversion[entry1] in s.entity_conversion[exit1].departure_counter)

    def test_right_priority_with_2_entries_2_exits(self):
        s = new_simulation()

        entry1 = entry_node().with_rate(0.2)
        s.add_node(entry1)
        entry2 = entry_node().with_rate(0.3)
        s.add_node(entry2)
        exit1 = exit_node()
        s.add_node(exit1)
        exit2 = exit_node()
        s.add_node(exit2)
        junction = right_priority_junction()
        s.add_node(junction)

        s.add_road(entry1.connect(Orientation.NORTH).to(junction).with_length(3))
        s.add_road(entry2.connect(Orientation.WEST).to(junction).with_length(3))
        s.add_road(junction.connect(Orientation.SOUTH).to(exit1).with_length(3))
        s.add_road(junction.connect(Orientation.EAST).to(exit2).with_length(3))

        s.add_path(entry1.to(exit1).with_proportion(30))
        s.add_path(entry1.to(exit2).with_proportion(70))
        s.add_path(entry2.to(exit1).with_proportion(70))
        s.add_path(entry2.to(exit2).with_proportion(30))

        random.seed(0)

        s.build_all()

        # --- Assertions ---
        simulator = s.simulator
        number_of_car = 0
        entry_nodes = [n for e in simulator.entities if type(e) is Entry for row in e.nodes for n in row]
        exit_nodes = [n for e in simulator.entities if type(e) is Exit for row in e.nodes for n in row]

        blocked_entry_nodes = set([])

        for _ in range(1000):
            # Subtracts cars that exit this turn
            number_of_car -= len([n for n in exit_nodes if n.current_car])
            simulator.tick()
            # Adds cars that appeared this turn
            entry_node_with_car = set([n for n in entry_nodes if n.current_car])
            number_of_car += len(entry_node_with_car - blocked_entry_nodes)
            blocked_entry_nodes = entry_node_with_car
            actual_number_of_car = len([n for e in simulator.entities for row in e.nodes for n in row if n.current_car])
            self.assertEqual(number_of_car, actual_number_of_car)

    def test_4_right_priority_with_4_entries_4_exits(self):
        s = new_simulation()

        entry1 = entry_node().with_rate(0.2)
        s.add_node(entry1)
        entry2 = entry_node().with_rate(0.3)
        s.add_node(entry2)
        entry3 = entry_node().with_rate(0.2)
        s.add_node(entry3)
        entry4 = entry_node().with_rate(0.3)
        s.add_node(entry4)

        exit1 = exit_node()
        s.add_node(exit1)
        exit2 = exit_node()
        s.add_node(exit2)
        exit3 = exit_node()
        s.add_node(exit3)
        exit4 = exit_node()
        s.add_node(exit4)

        junction1 = right_priority_junction()
        s.add_node(junction1)
        junction2 = right_priority_junction()
        s.add_node(junction2)
        junction3 = right_priority_junction()
        s.add_node(junction3)
        junction4 = right_priority_junction()
        s.add_node(junction4)

        s.add_road(entry1.connect(Orientation.SOUTH).to(junction1).with_length(3))
        s.add_road(junction1.connect(Orientation.WEST).to(exit1).with_length(3))
        s.add_road(junction1.connect(Orientation.EAST).to(junction2).with_length(7))

        
        s.add_road(entry2.connect(Orientation.WEST).to(junction2).with_length(3))
        s.add_road(junction2.connect(Orientation.NORTH).to(exit2).with_length(3))
        s.add_road(junction2.connect(Orientation.SOUTH).to(junction3).with_length(7))

        s.add_road(entry3.connect(Orientation.NORTH).to(junction3).with_length(3))
        s.add_road(junction3.connect(Orientation.EAST).to(exit3).with_length(3))
        s.add_road(junction3.connect(Orientation.WEST).to(junction4).with_length(7))

        s.add_road(entry4.connect(Orientation.EAST).to(junction4).with_length(3))
        s.add_road(junction4.connect(Orientation.SOUTH).to(exit4).with_length(3))
        s.add_road(junction4.connect(Orientation.NORTH).to(junction1).with_length(7))

        s.add_path(entry1.to(exit1).with_proportion(25))
        s.add_path(entry1.to(exit2).with_proportion(25))
        s.add_path(entry1.to(exit3).with_proportion(25))
        s.add_path(entry1.to(exit4).with_proportion(25))
        
        s.add_path(entry2.to(exit2).with_proportion(25))
        s.add_path(entry2.to(exit3).with_proportion(25))
        s.add_path(entry2.to(exit4).with_proportion(25))
        s.add_path(entry2.to(exit1).with_proportion(25))
        
        s.add_path(entry3.to(exit3).with_proportion(25))
        s.add_path(entry3.to(exit4).with_proportion(25))
        s.add_path(entry3.to(exit1).with_proportion(25))
        s.add_path(entry3.to(exit2).with_proportion(25))
        
        s.add_path(entry4.to(exit4).with_proportion(25))
        s.add_path(entry4.to(exit1).with_proportion(25))
        s.add_path(entry4.to(exit2).with_proportion(25))
        s.add_path(entry4.to(exit3).with_proportion(25))

        random.seed(0)

        s.build_all()

        # --- Assertions ---
        simulator = s.simulator
        number_of_car = 0
        entry_nodes = [n for e in simulator.entities if type(e) is Entry for row in e.nodes for n in row]
        exit_nodes = [n for e in simulator.entities if type(e) is Exit for row in e.nodes for n in row]

        blocked_entry_nodes = set([])

        for _ in range(1000):
            # Subtracts cars that exit this turn
            number_of_car -= len([n for n in exit_nodes if n.current_car])
            simulator.tick()
            # Adds cars that appeared this turn
            entry_node_with_car = set([n for n in entry_nodes if n.current_car])
            number_of_car += len(entry_node_with_car - blocked_entry_nodes)
            blocked_entry_nodes = entry_node_with_car
            actual_number_of_car = len([n for e in simulator.entities for row in e.nodes for n in row if n.current_car])
            self.assertEqual(number_of_car, actual_number_of_car)

    def test_right_priority_with_4_entries_4_exits_5_ways_per_node(self):
        s = new_simulation()

        entry1 = entry_node().with_rate(0.2)
        s.add_node(entry1)
        entry2 = entry_node().with_rate(0.3)
        s.add_node(entry2)
        entry3 = entry_node().with_rate(0.2)
        s.add_node(entry1)
        entry4 = entry_node().with_rate(0.3)
        s.add_node(entry2)

        exit1 = exit_node()
        s.add_node(exit1)
        exit2 = exit_node()
        s.add_node(exit2)
        exit3 = exit_node()
        s.add_node(exit1)
        exit4 = exit_node()
        s.add_node(exit2)

        junction = right_priority_junction()
        s.add_node(junction)

        s.add_road(entry1.connect(Orientation.NORTH).to(junction).with_length(3).with_n_ways(3))
        s.add_road(entry2.connect(Orientation.WEST).to(junction).with_length(3).with_n_ways(3))
        s.add_road(entry3.connect(Orientation.NORTH).to(junction).with_length(3).with_n_ways(3))
        s.add_road(entry4.connect(Orientation.WEST).to(junction).with_length(3).with_n_ways(3))
        s.add_road(junction.connect(Orientation.SOUTH).to(exit1).with_length(3).with_n_ways(3))
        s.add_road(junction.connect(Orientation.EAST).to(exit2).with_length(3).with_n_ways(3))
        s.add_road(junction.connect(Orientation.SOUTH).to(exit3).with_length(3).with_n_ways(3))
        s.add_road(junction.connect(Orientation.EAST).to(exit4).with_length(3).with_n_ways(3))

        s.add_path(entry1.go_through(junction, exit1).with_proportion(30))
        s.add_path(entry1.go_through(junction, exit2).with_proportion(70))
        s.add_path(entry2.go_through(junction, exit1).with_proportion(70))
        s.add_path(entry2.go_through(junction, exit2).with_proportion(30))
        s.add_path(entry3.go_through(junction, exit1).with_proportion(30))
        s.add_path(entry3.go_through(junction, exit2).with_proportion(70))
        s.add_path(entry4.go_through(junction, exit1).with_proportion(70))
        s.add_path(entry4.go_through(junction, exit2).with_proportion(30))

        random.seed(0)

        s.build_all()

        # --- Assertions ---
        simulator = s.simulator
        number_of_car = 0
        entry_nodes = [n for e in simulator.entities if type(e) is Entry for row in e.nodes for n in row]
        exit_nodes = [n for e in simulator.entities if type(e) is Exit for row in e.nodes for n in row]

        blocked_entry_nodes = set([])

        for _ in range(1000):
            # Subtracts cars that exit this turn
            number_of_car -= len([n for n in exit_nodes if n.current_car])
            simulator.tick()
            # Adds cars that appeared this turn
            entry_node_with_car = set([n for n in entry_nodes if n.current_car])
            number_of_car += len(entry_node_with_car - blocked_entry_nodes)
            blocked_entry_nodes = entry_node_with_car
            actual_number_of_car = len([n for e in simulator.entities for row in e.nodes for n in row if n.current_car])
            self.assertEqual(number_of_car, actual_number_of_car)



if __name__ == '__main__':
    unittest.main()