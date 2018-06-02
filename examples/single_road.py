from modeler import *
from shared import Orientation


def main():
    s = new_simulation()

    e1 = entry_node().with_rate(0.2)
    s.add_node(e1)
    e2 = exit_node()
    s.add_node(e2)

    s.add_road(e1.connect(Orientation.NORTH).to(e2).with_length(20))

    s.add_path(e1.go_through(e2).with_proportion(100))

    s.run_for(50)


if __name__ == '__main__':
    main()