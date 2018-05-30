from modeler.entry_node import EntryNode
from modeler.exit_node import ExitNode

nodes = []

def entry_node():
    node = EntryNode()
    nodes.append(node)
    return node

def exit_node():
    node = ExitNode()
    nodes.append(node)
    return node

simulate