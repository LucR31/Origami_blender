from .crease import CreaseEdge
from typing import List
from bmesh.types import BMesh


def get_valid_creases(bm: BMesh, obj) -> List[CreaseEdge]:
    creases = []

    for c in obj.origami_creases:
        if c.edge_index >= len(bm.edges):
            continue

        edge = bm.edges[c.edge_index]

        creases.append(CreaseEdge(edge=edge, angle=c.angle, crease_type=c.crease_type))

    return creases
