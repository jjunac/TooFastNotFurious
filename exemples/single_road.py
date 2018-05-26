import modeler as m

def main():
    m.createRoad()\
        .that_starts(m.createEntryNode())\
        .that_ends(m.createExitNode())\
        .with_length(5)

if __name__ == '__main__':
    main()