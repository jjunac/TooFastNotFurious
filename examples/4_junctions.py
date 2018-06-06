from modeler import *
from shared import Orientation


def main():
    s = new_simulation()

    entry1 = entry_node().with_rate(0.8)
    s.add_node(entry1)
    entry2 = entry_node().with_rate(0.8)
    s.add_node(entry2)
    entry3 = entry_node().with_rate(0.8)
    s.add_node(entry3)
    entry4 = entry_node().with_rate(0.8)
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

    s.add_path(entry1.go_through(junction1, exit1).with_proportion(25))
    s.add_path(entry1.go_through(junction1, junction2, exit2).with_proportion(25))
    s.add_path(entry1.go_through(junction1, junction2, junction3, exit3).with_proportion(25))
    s.add_path(entry1.go_through(junction1, junction2, junction3, junction4, exit4).with_proportion(25))

    s.add_path(entry2.go_through(junction2, exit2).with_proportion(25))
    s.add_path(entry2.go_through(junction2, junction3, exit3).with_proportion(25))
    s.add_path(entry2.go_through(junction2, junction3, junction4, exit4).with_proportion(25))
    s.add_path(entry2.go_through(junction2, junction3, junction4, junction1, exit1).with_proportion(25))

    s.add_path(entry3.go_through(junction3, exit3).with_proportion(25))
    s.add_path(entry3.go_through(junction3, junction4, exit4).with_proportion(25))
    s.add_path(entry3.go_through(junction3, junction4, junction1, exit1).with_proportion(25))
    s.add_path(entry3.go_through(junction3, junction4, junction1, junction2, exit2).with_proportion(25))

    s.add_path(entry4.go_through(junction4, exit4).with_proportion(25))
    s.add_path(entry4.go_through(junction4, junction1, exit1).with_proportion(25))
    s.add_path(entry4.go_through(junction4, junction1, junction2, exit2).with_proportion(25))
    s.add_path(entry4.go_through(junction4, junction1, junction2, junction3, exit3).with_proportion(25))

    s.run_graphical_for(1000)


if __name__ == '__main__':
    main()
