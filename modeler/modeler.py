from modeler.entry_node import EntryNode
from modeler.exit_node import ExitNode
from modeler.path import Path
from modeler.simulation import Simulation

nodes = []

def entry_node():
    node = EntryNode()
    nodes.append(node)
    return node

def exit_node():
    node = ExitNode()
    nodes.append(node)
    return node

def new_simulation():
    return Simulation()

def go_to(destination):
    return Path(destination)