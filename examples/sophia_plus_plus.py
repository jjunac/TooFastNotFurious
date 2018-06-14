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
    entry1 = entry_node().with_rate(0.2)
    s.add_node(entry1)
    entry2 = entry_node().with_rate(0.3)
    s.add_node(entry2)

    carrefour_out = exit_node()
    s.add_node(carrefour_out)
    sophia_out = exit_node()
    s.add_node(sophia_out)
    juan_out = exit_node()
    s.add_node(juan_out)
    exit1 = exit_node()
    s.add_node(exit1)
    exit2 = exit_node()
    s.add_node(exit2)

    rondpoint1 = roundabout().with_n_ways(2)
    s.add_node(rondpoint1)
    feu_rouge1 = traffic_light()
    feu_rouge1.set_state1_orientations(Orientation.EAST, Orientation.WEST).with_timer(13)
    feu_rouge1.set_state2_orientations(Orientation.EAST, Orientation.WEST).with_timer(11)
    feu_rouge1.with_interval(5)
    s.add_node(feu_rouge1)


    s.add_road(carrefour_in.connect(Orientation.WEST).to(rondpoint1).with_length(2).with_n_ways(2))
    s.add_road(rondpoint1.connect(Orientation.EAST).to(carrefour_out).with_length(2).with_n_ways(2))

    s.add_road(sophia_in.connect(Orientation.SOUTH).to(rondpoint1).with_length(2).with_n_ways(2))
    s.add_road(rondpoint1.connect(Orientation.NORTH).to(sophia_out).with_length(2).with_n_ways(2))

    s.add_road(juan_in.connect(Orientation.NORTH).to(rondpoint1).with_length(2).with_n_ways(2))
    s.add_road(rondpoint1.connect(Orientation.SOUTH).to(juan_out).with_length(2).with_n_ways(2))


    s.add_road(feu_rouge1.connect(Orientation.EAST).to(rondpoint1).with_length(2).with_n_ways(2))
    s.add_road(rondpoint1.connect(Orientation.WEST).to(feu_rouge1).with_length(2).with_n_ways(2))


    s.add_road(entry1.connect(Orientation.SOUTH).to(feu_rouge1).with_length(2).with_n_ways(2))
    s.add_road(feu_rouge1.connect(Orientation.NORTH).to(exit1).with_length(2).with_n_ways(2))

    s.add_road(entry2.connect(Orientation.NORTH).to(feu_rouge1).with_length(2).with_n_ways(2))
    s.add_road(feu_rouge1.connect(Orientation.SOUTH).to(exit2).with_length(2).with_n_ways(2))


    s.add_path(carrefour_in.to(sophia_out).with_proportion(30))
    s.add_path(carrefour_in.to(juan_out).with_proportion(30))
    s.add_path(carrefour_in.to(exit1).with_proportion(40))

    s.add_path(sophia_in.to(carrefour_out).with_proportion(30))
    s.add_path(sophia_in.to(juan_out).with_proportion(30))
    s.add_path(sophia_in.to(exit2).with_proportion(40))

    s.add_path(juan_in.to(sophia_out).with_proportion(30))
    s.add_path(juan_in.to(carrefour_out).with_proportion(30))
    s.add_path(juan_in.to(exit1).with_proportion(40))

    s.run_graphical_for(400)


if __name__ == '__main__':
    main()
