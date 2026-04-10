from mathutils import Vector, Matrix
from bmesh.types import BMVert, BMFace, BMEdge
from typing import Optional, List
import math


def rotate_face_around_edge(
    face: BMFace, v1: BMVert, v2: BMVert, angle_rad: float
) -> None:
    """
    Rotate a face around the edge defined by v1-v2 by angle_rad (radians).
    Vertices on the edge remain fixed.
    """
    edge_vec: Vector = (v2.co - v1.co).normalized()
    rot: Matrix = Matrix.Rotation(angle_rad, 3, edge_vec)

    for v in face.verts:
        if v not in (v1, v2):
            v.co = rot @ (v.co - v1.co) + v1.co


def compute_face_normal(face: BMFace) -> Vector:
    """Compute face normal (safe version)"""
    return face.normal.normalized()


def compute_dihedral_angle(v1: BMVert, v2: BMVert, f1: BMFace, f2: BMFace) -> float:
    """
    Compute signed dihedral angle between two faces sharing edge (v1, v2)
    """

    n1 = compute_face_normal(f1)
    n2 = compute_face_normal(f2)

    edge_vec = (v2.co - v1.co).normalized()

    # Angle magnitude
    cos_theta = max(-1.0, min(1.0, n1.dot(n2)))
    theta = math.acos(cos_theta)

    # Sign using orientation
    sign = 1.0 if edge_vec.dot(n1.cross(n2)) > 0 else -1.0

    return sign * theta
