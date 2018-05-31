from modeler import *

def main():
    s = new_simulation()

    e1 = entry_node()
    s.add_node(e1)
    e2 = exit_node()
    s.add_node(e2)

    s.add_road(e1.connect(Orientation.NORTH).to(e2).with_length(20))

    s.run_for(50)

if __name__ == '__main__':
    main()