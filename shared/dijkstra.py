def dijkstra(nodes, weights, source):
    '''
    Computes all shortest paths frm source to all other vertices.
    Returns a dictionary 'path' such that if path[n] = u, u is the
    predecessor of n on the shortest path form source to n
    '''
    known = set()
    path = {}
    values = {}
    to_compute = []
    for n in nodes:
        values[n] = float('inf')
        to_compute.append(n)
    values[source] = 0
    while to_compute:
        n = min(to_compute, key=lambda n: values[n])
        to_compute.remove(n)
        known.add(n)
        for a in n.successors:
            if a not in known and values[n] + weights[(n, a)] < values[a]:
                values[a] = values[n] + weights[(n, a)]
                path[a] = n
    return path

def reconstruct_path(paths, source, destination):
    nodes = []
    d = destination
    while d != source:
        nodes.append(d)
        d = paths[d]
    return reversed(nodes)

def dijkstra_with_path(nodes, weights, source, destination):
    return reconstruct_path(dijkstra(nodes, weights, source), source, destination)