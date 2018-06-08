from modeler import *
from shared import Orientation


def main():
    s = new_simulation()

    entry1 = entry_node().with_rate(0.2)
    s.add_node(entry1)
    entry2 = entry_node().with_rate(0.3)
    s.add_node(entry2)
    entry3 = entry_node().with_rate(0.2)
    s.add_node(entry3)

    exit3 = exit_node()
    s.add_node(exit3)
    exit4 = exit_node()
    s.add_node(exit4)
    exit5 = exit_node()
    s.add_node(exit5)

    junction1 = right_priority_junction()
    s.add_node(junction1)
    junction2 = right_priority_junction()
    s.add_node(junction2)

    s.add_road(entry1.connect(Orientation.NORTH).to(junction1).with_length(3).with_n_ways(2))
    s.add_road(entry2.connect(Orientation.SOUTH).to(junction1).with_length(3).with_n_ways(2))
    s.add_road(entry3.connect(Orientation.EAST).to(junction1).with_length(4).with_n_ways(2))

    s.add_road(junction1.connect(Orientation.EAST).to(junction2).with_length(7).with_n_ways(2))

    s.add_road(junction2.connect(Orientation.EAST).to(exit3).with_length(4).with_n_ways(2))
    s.add_road(junction2.connect(Orientation.NORTH).to(exit4).with_length(3).with_n_ways(2))
    s.add_road(junction2.connect(Orientation.SOUTH).to(exit5).with_length(3).with_n_ways(2))

    s.add_path(entry1.to(exit3).with_proportion(40))
    s.add_path(entry1.to(exit4).with_proportion(30))
    s.add_path(entry1.to(exit5).with_proportion(30))

    s.add_path(entry2.to(exit3).with_proportion(40))
    s.add_path(entry2.to(exit4).with_proportion(30))
    s.add_path(entry2.to(exit5).with_proportion(30))

    s.add_path(entry3.to(exit3).with_proportion(40))
    s.add_path(entry3.to(exit4).with_proportion(30))
    s.add_path(entry3.to(exit5).with_proportion(30))

    s.run_graphical_for(400)


if __name__ == '__main__':
    main()
