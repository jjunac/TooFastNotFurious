from simulator.road_node import RoadNode


def build_road(length, orientation):
    res = [RoadNode(orientation)]
    for i in range(length - 1):
        res.append(RoadNode(orientation))
        res[-2].successors.append(res[-1])
        res[-1].predecessors.append(res[-2])
    return res


def compute_next(road):
    for n in road:
        n.compute_next()


def apply_next(road):
    for n in road:
        n.apply_next()