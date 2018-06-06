# TODO rename to link_node
def link(predecessor, successor):
    predecessor.successors.append(successor)
    successor.predecessors.append(predecessor)
