from modeler import *
from shared import Orientation


def main():
    s = new_simulation()

    entry1 = entry_node().with_rate(0.2)
    s.add_node(entry1)
    entry2 = entry_node().with_rate(0.3)
    s.add_node(entry2)
    entry3 = entry_node().with_rate(0.4)
    s.add_node(entry3)
    entry4 = entry_node().with_rate(0.2)
    s.add_node(entry4)
    exit1 = exit_node()
    s.add_node(exit1)
    exit2 = exit_node()
    s.add_node(exit2)
    exit3 = exit_node()
    s.add_node(exit3)
    exit4 = exit_node()
    s.add_node(exit4)

    ra = roundabout().with_n_ways(2)
    s.add_node(ra)

    s.add_road(entry1.connect(Orientation.EAST).to(ra).with_length(2))
    s.add_road(ra.connect(Orientation.WEST).to(exit1).with_length(2))

    s.add_road(entry2.connect(Orientation.SOUTH).to(ra).with_length(2))
    s.add_road(ra.connect(Orientation.NORTH).to(exit2).with_length(2))

    s.add_road(entry3.connect(Orientation.WEST).to(ra).with_length(2))
    s.add_road(ra.connect(Orientation.EAST).to(exit3).with_length(2))

    s.add_road(entry4.connect(Orientation.NORTH).to(ra).with_length(2))
    s.add_road(ra.connect(Orientation.SOUTH).to(exit4).with_length(2))

    s.add_path(entry1.to(exit2).with_proportion(30))
    s.add_path(entry1.to(exit3).with_proportion(30))
    s.add_path(entry1.to(exit4).with_proportion(40))

    s.add_path(entry2.to(exit1).with_proportion(30))
    s.add_path(entry2.to(exit3).with_proportion(30))
    s.add_path(entry2.to(exit4).with_proportion(40))

    s.add_path(entry3.to(exit2).with_proportion(30))
    s.add_path(entry3.to(exit1).with_proportion(30))
    s.add_path(entry3.to(exit4).with_proportion(40))

    s.add_path(entry4.to(exit2).with_proportion(30))
    s.add_path(entry4.to(exit3).with_proportion(30))
    s.add_path(entry4.to(exit1).with_proportion(40))
    s.run_graphical_for(400)


if __name__ == '__main__':
    main()
