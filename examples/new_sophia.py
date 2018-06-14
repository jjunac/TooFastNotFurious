from modeler import *
from shared import Orientation


def main():
    s = new_simulation()

    carrefour_in = entry_node().with_rate(0.4)
    s.add_node(carrefour_in)
    carrefour_out = exit_node()
    s.add_node(carrefour_out)
    juan_in = entry_node().with_rate(0.4)
    s.add_node(juan_in)
    juan_out = exit_node()
    s.add_node(juan_out)
    valmasque_in = entry_node().with_rate(0.4)
    s.add_node(valmasque_in)
    valmasque_out = exit_node()
    s.add_node(valmasque_out)

    sophia_in = entry_node().with_rate(0.4)
    s.add_node(sophia_in)
    sophia_out = exit_node()
    s.add_node(sophia_out)
    trois_moulins_in = entry_node().with_rate(0.4)
    s.add_node(trois_moulins_in)
    trois_moulins_out = exit_node()
    s.add_node(trois_moulins_out)
    bus_in = entry_node().with_rate(0.15)
    s.add_node(bus_in)
    bus_out = exit_node()
    s.add_node(bus_out)

    rondpoint1 = roundabout().with_n_ways(2)
    s.add_node(rondpoint1)

    rondpoint2 = roundabout().with_n_ways(2)
    s.add_node(rondpoint2)


    s.add_road(carrefour_in.connect(Orientation.WEST).to(rondpoint1).with_length(2).with_n_ways(2))
    s.add_road(rondpoint1.connect(Orientation.EAST).to(carrefour_out).with_length(2).with_n_ways(2))

    s.add_road(juan_in.connect(Orientation.NORTH).to(rondpoint1).with_length(2).with_n_ways(2))
    s.add_road(rondpoint1.connect(Orientation.SOUTH).to(juan_out).with_length(2).with_n_ways(2))

    s.add_road(valmasque_in.connect(Orientation.EAST).to(rondpoint1).with_length(2).with_n_ways(2))
    s.add_road(rondpoint1.connect(Orientation.WEST).to(valmasque_out).with_length(2).with_n_ways(2))


    s.add_road(rondpoint2.connect(Orientation.SOUTH).to(rondpoint1).with_length(10).with_n_ways(2))
    s.add_road(rondpoint1.connect(Orientation.NORTH).to(rondpoint2).with_length(10).with_n_ways(2))


    s.add_road(trois_moulins_in.connect(Orientation.WEST).to(rondpoint2).with_length(2).with_n_ways(2))
    s.add_road(rondpoint2.connect(Orientation.EAST).to(trois_moulins_out).with_length(2).with_n_ways(2))

    s.add_road(sophia_in.connect(Orientation.SOUTH).to(rondpoint2).with_length(2).with_n_ways(2))
    s.add_road(rondpoint2.connect(Orientation.NORTH).to(sophia_out).with_length(2).with_n_ways(2))

    s.add_road(bus_in.connect(Orientation.EAST).to(rondpoint2).with_length(2).with_n_ways(2))
    s.add_road(rondpoint2.connect(Orientation.WEST).to(bus_out).with_length(2).with_n_ways(2))



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
