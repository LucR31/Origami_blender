def get_valid_creases(bm, obj):
    creases = []

    for c in obj.origami_creases:
        if c.edge_index < len(bm.edges):
            creases.append(c)

    return creases