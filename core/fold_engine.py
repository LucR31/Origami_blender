import math
from bmesh.types import BMEdge

from .crease_manager import get_valid_creases
from .constrains import satisfy_crease_constraint, satisfy_edge_constraint
from .edge_utils import get_edge_faces, rotate_face_around_edge
from .utils import store_original_positions, restore_original_positions

def apply_single_fold(bm, crease:BMEdge) -> None:

    edge = bm.edges[crease.edge_index]
    v1, v2 = edge.verts

    flap_face = get_edge_faces(edge)[0]
    if flap_face is None:
        return

    angle = math.radians(crease.angle)
    if crease.crease_type == "MOUNTAIN":
        angle = -angle

    rotate_face_around_edge(flap_face, v1, v2, angle)


def apply_all_folds(bm, obj):
    # Store original once
    if not obj.origami_original_positions:
        store_original_positions(bm, obj)

    # Reset mesh
    restore_original_positions(bm, obj)

    creases = get_valid_creases(bm, obj)

    for crease in creases:
        apply_single_fold(bm, crease)


def apply_constraint_fold(bm, crease: BMEdge, iterations: int = 5) -> None:
    
    edge = bm.edges[crease.edge_index]
    v1, v2 = edge.verts
    faces = get_edge_faces(edge)
    if not faces:
        return  # skip border edges
    f1, f2 = faces[0], faces[1]

    target_angle = math.radians(crease.angle)
    if crease.crease_type == "MOUNTAIN":
        target_angle = -target_angle

    for _ in range(iterations):
        satisfy_crease_constraint(v1, v2, f1, f2, target_angle)
        for e in f1.edges + f2.edges:
            L = (e.verts[0].co - e.verts[1].co).length
            satisfy_edge_constraint(e.verts[0], e.verts[1], L)


def apply_all_constraints(bm, obj, iterations:int = 3) -> None:
    restore_original_positions(bm, obj)
    creases = get_valid_creases(bm, obj)
    for _ in range(iterations):
        for crease in creases:
            apply_constraint_fold(bm, crease)
