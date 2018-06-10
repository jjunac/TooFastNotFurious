from modeler import *
from shared import Orientation


def main():
    s = new_simulation()

    entry1 = entry_node().with_rate(0.2)
    s.add_node(entry1)
    exit1 = exit_node()
    s.add_node(exit1)
    exit2 = exit_node()
    s.add_node(exit2)
    junction = right_priority()
    s.add_node(junction)

    s.add_road(entry1.connect(Orientation.NORTH).to(junction).with_length(1))
    s.add_road(junction.connect(Orientation.NORTH).to(exit1).with_length(1))
    s.add_road(junction.connect(Orientation.WEST).to(exit2).with_length(1))

    s.add_path(entry1.to(exit1).with_proportion(30))
    s.add_path(entry1.to(exit2).with_proportion(70))

    s.run_graphical_for(400)


if __name__ == '__main__':
    main()
