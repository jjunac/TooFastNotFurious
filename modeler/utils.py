from shared import DijkstraHeap

def dijkstra(nodes, source):
    '''
    Computes all shortest paths frm source to all other vertices.
    Returns a dictionary 'path' such that if path[n] = u, u is the
    predecessor of n on the shortest path form source to n
    '''
    known = set()
    path = {}
    values = {}
    # heap = DijkstraHeap()
    to_compute = []
    for n in nodes:
        values[n] = float('inf')
        # heap.add(n)
        to_compute.append(n)
    values[source] = 0
    # heap.decreaseKey(source)
    # while len(heap) > 0:
    while to_compute:
        # n = heap.pop()
        n = min(to_compute, key=lambda n: values[n])
        to_compute.remove(n)
        known.add(n)
        for a in n.successors:
            if a not in known:
                # TODO change weight of edges to improve the path
                if values[n] + 1 < values[a]:
                    values[a] = values[n] + 1
                    # heap.decreaseKey(a)
                    path[a] = n
    return path

def reconstruct_path(paths, source, destination):
    nodes = []
    d = destination
    while d != source:
        nodes.append(d)
        d = paths[d]
    return nodes
