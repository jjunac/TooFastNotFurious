def compute_next(road):
    for n in road:
        n.compute_next()


def apply_next(road):
    for n in road:
        n.apply_next()


def link(predecessor, successor):
    predecessor.successors.append(successor)
    successor.predecessors.append(predecessor)
