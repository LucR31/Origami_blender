def get_selected_edge(bm):
    edges = [e for e in bm.edges if e.select]
    return edges[0] if len(edges) == 1 else None