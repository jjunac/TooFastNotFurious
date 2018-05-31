from simulator.road_node import RoadNode


def build_road(length, orientation):
    res = [RoadNode(orientation)]
    for i in range(length - 1):
        res.append(RoadNode(orientation))
        link(res[-2], res[-1])
    return res


def compute_next(road):
    for n in road:
        n.compute_next()


def apply_next(road):
    for n in road:
        n.apply_next()


def link(predecessor, successor):
    predecessor.successors.append(successor)
    successor.predecessors.append(predecessor)
