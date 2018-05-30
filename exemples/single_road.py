from modeler import *

def main():
    s = entry_node()
    t = exit_node()

    s.connect(Orientation.NORTH).to(t).with_length(8)

if __name__ == '__main__':
    main()