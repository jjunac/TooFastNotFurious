from modeler import *
from shared import Orientation


def main():
    s = new_simulation()

    entry1 = entry_node().with_rate(0.2)
    s.add_node(entry1)
    entry2 = entry_node().with_rate(0.3)
    s.add_node(entry2)
    exit1 = exit_node()
    s.add_node(exit1)
    exit2 = exit_node()
    s.add_node(exit2)
    junction = traffic_light().set_state1_orientations(Orientation.EAST).with_timer(5)
    junction.set_state2_orientations(Orientation.SOUTH).with_timer(5)
    junction.with_interval(2)
    s.add_node(junction)

    s.add_road(entry1.connect(Orientation.NORTH).to(junction).with_length(3))
    s.add_road(entry2.connect(Orientation.WEST).to(junction).with_length(3))
    s.add_road(junction.connect(Orientation.NORTH).to(exit1).with_length(3))
    s.add_road(junction.connect(Orientation.WEST).to(exit2).with_length(3))

    s.add_path(entry1.to(exit1).with_proportion(30))
    s.add_path(entry1.to(exit2).with_proportion(70))
    s.add_path(entry2.to(exit1).with_proportion(70))
    s.add_path(entry2.to(exit2).with_proportion(30))

    s.run_graphical_for(400)


if __name__ == '__main__':
    main()
