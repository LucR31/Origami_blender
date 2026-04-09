from mathutils import Vector, Matrix
from bmesh.types import BMVert, BMFace, BMEdge
from typing import Optional, List


def get_edge_faces(edge: BMEdge) -> Optional[List[BMFace]]:
    """
    Return the face/s that should rotate around this edge.
    Assumes exactly two faces per crease edge, skips otherwise.
    """
    if len(edge.link_faces) != 2:
        return None

    f1, f2 = edge.link_faces
    return [f1, f2]


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
