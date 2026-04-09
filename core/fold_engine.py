import math
import bmesh
from mathutils import Matrix
from typing import Optional, Set, List, Tuple
from bmesh.types import BMEdge, BMFace, BMVert
from .crease_manager import get_valid_creases
from .constrains import satisfy_crease_constraint, satisfy_edge_constraint


def get_edge_faces(edge: BMEdge) -> Optional[List[BMFace]]:
    """
    Return the face/s that should rotate around this edge.
    Assumes exactly two faces per crease edge, skips otherwise.
    """
    if len(edge.link_faces) != 2:
        return None

    f1, f2 = edge.link_faces
    return [f1, f2]


def store_original_positions(bm, obj) -> None:
    coords = []
    for v in bm.verts:
        coords.append(f"{v.co.x},{v.co.y},{v.co.z}")

    obj.origami_original_positions = "|".join(coords)


def restore_original_positions(bm, obj) -> None:
    if not obj.origami_original_positions:
        store_original_positions(bm, obj)
        return

    coords = obj.origami_original_positions.split("|")

    for v, c in zip(bm.verts, coords):
        x, y, z = map(float, c.split(","))
        v.co.x = x
        v.co.y = y
        v.co.z = z


def apply_single_fold(bm, crease):

    edge = bm.edges[crease.edge_index]
    v1, v2 = edge.verts
    axis = (v2.co - v1.co).normalized()
    pivot = (v1.co + v2.co) / 2

    # Pick flap face
    rotate_mountain = crease.crease_type == "MOUNTAIN"
    flap_face = get_edge_faces(edge, rotate_mountain)[0]
    if flap_face is None:
        return

    # Only rotate vertices in flap_face
    verts_to_rotate = set(flap_face.verts)

    angle = math.radians(crease.angle)
    if crease.crease_type == "MOUNTAIN":
        angle = -angle

    rot = Matrix.Rotation(angle, 3, axis)
    for v in verts_to_rotate:
        v.co = rot @ (v.co - pivot) + pivot


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
