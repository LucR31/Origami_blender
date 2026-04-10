import math
from bmesh.types import BMVert, BMFace, BMesh
from .edge_utils import rotate_face_around_edge
from abc import ABC, abstractmethod


class Constraint(ABC):
    """
    Base class for all constraints.
    """

    @abstractmethod
    def project(self, bm: BMesh) -> None:
        pass


class EdgeLengthConstraint(Constraint):
    def __init__(self, edge, rest_length: float) -> None:
        self.edge = edge
        self.rest_length = rest_length

    def project(self, bm) -> None:
        v1, v2 = self.edge.verts

        delta = v2.co - v1.co
        d = delta.length

        if d == 0:
            return

        diff = (d - self.rest_length) / 2
        correction = delta.normalized() * diff

        v1.co += correction
        v2.co -= correction


class CreaseConstraint(Constraint):
    def __init__(self, crease_edge) -> None:
        self.crease = crease_edge

    def project(self, bm) -> None:
        faces = self.crease.get_faces()
        if faces is None:
            return

        flap_face, fixed_face = faces
        v1, v2 = self.crease.edge.verts

        current = self.crease.compute_dihedral()
        target = math.radians(self.crease.signed_angle())

        diff = current - target

        rotate_face_around_edge(flap_face, v1, v2, -diff)


# --- DEPRECATED ---
def satisfy_edge_constraint(v1: BMVert, v2: BMVert, L: float) -> None:
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
