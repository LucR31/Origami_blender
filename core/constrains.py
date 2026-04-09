import math
from bmesh.types import BMVert, BMFace
from .edge_utils import rotate_face_around_edge


def satisfy_edge_constraint(v1: BMVert, v2: BMVert, L:float) -> None:
    delta = v2.co - v1.co
    d = delta.length
    if d == 0:
        return
    diff = (d - L) / 2
    correction = delta.normalized() * diff
    v1.co += correction
    v2.co -= correction


def satisfy_crease_constraint(
    v1: BMVert, v2: BMVert, face1: BMFace, face2: BMFace, target_angle: float
) -> None:
    # Compute current dihedral angle
    n1 = face1.normal
    n2 = face2.normal
    current_angle = math.acos(max(-1, min(1, n1.dot(n2))))

    # Difference
    diff = target_angle - current_angle

    # Simple rotation of one face around edge
    rotate_face_around_edge(face2, v1, v2, diff)
