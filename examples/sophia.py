from modeler import *
from shared import Orientation


def main():
    s = new_simulation()

    carrefour_in = entry_node().with_rate(0.4)
    s.add_node(carrefour_in)
    sophia_in = entry_node().with_rate(0.4)
    s.add_node(sophia_in)
    juan_in = entry_node().with_rate(0.4)
    s.add_node(juan_in)
    valmasque_in = entry_node().with_rate(0.4)
    s.add_node(valmasque_in)
    carrefour_out = exit_node()
    s.add_node(carrefour_out)
    sophia_out = exit_node()
    s.add_node(sophia_out)
    juan_out = exit_node()
    s.add_node(juan_out)
    valmasque_out = exit_node()
    s.add_node(valmasque_out)

    rondpoint1 = roundabout().with_n_ways(2)
    s.add_node(rondpoint1)

    s.add_road(carrefour_in.connect(Orientation.WEST).to(rondpoint1).with_length(2).with_n_ways(2))
    s.add_road(rondpoint1.connect(Orientation.EAST).to(carrefour_out).with_length(2).with_n_ways(2))

    s.add_road(sophia_in.connect(Orientation.SOUTH).to(rondpoint1).with_length(2).with_n_ways(2))
    s.add_road(rondpoint1.connect(Orientation.NORTH).to(sophia_out).with_length(2).with_n_ways(2))

    s.add_road(juan_in.connect(Orientation.NORTH).to(rondpoint1).with_length(2).with_n_ways(2))
    s.add_road(rondpoint1.connect(Orientation.SOUTH).to(juan_out).with_length(2).with_n_ways(2))

    s.add_road(valmasque_in.connect(Orientation.EAST).to(rondpoint1).with_length(2).with_n_ways(2))
    s.add_road(rondpoint1.connect(Orientation.WEST).to(valmasque_out).with_length(2).with_n_ways(2))

    s.add_path(carrefour_in.to(sophia_out).with_proportion(30))
    s.add_path(carrefour_in.to(juan_out).with_proportion(30))
    s.add_path(carrefour_in.to(valmasque_out).with_proportion(40))

    s.add_path(sophia_in.to(carrefour_out).with_proportion(30))
    s.add_path(sophia_in.to(juan_out).with_proportion(30))
    s.add_path(sophia_in.to(valmasque_out).with_proportion(40))

    s.add_path(juan_in.to(sophia_out).with_proportion(30))
    s.add_path(juan_in.to(carrefour_out).with_proportion(30))
    s.add_path(juan_in.to(valmasque_out).with_proportion(40))

    s.add_path(valmasque_in.to(sophia_out).with_proportion(30))
    s.add_path(valmasque_in.to(juan_out).with_proportion(30))
    s.add_path(valmasque_in.to(carrefour_out).with_proportion(40))
    s.run_graphical_for(400)


if __name__ == '__main__':
    main()
