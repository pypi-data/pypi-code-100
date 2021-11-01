def ancestors(g, graph):
    """
    Extract ancestors nodes from an starting node
    :param g: starting node name
    :param graph: Graph
    :return: a set with node names
    """
    result = {g}
    for o in graph.successors(g):
        result.update(ancestors(o, graph))
    return result
