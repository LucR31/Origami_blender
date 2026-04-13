import math
from bmesh.types import BMVert, BMFace, BMesh
from .edge_utils import rotate_face_around_edge
from abc import ABC, abstractmethod


class Constraint(ABC):
    """
    Base class for all constraints.
    """
    def __init__(self, weight:float = 1.0) -> None:
        self.weight = weight

    @abstractmethod
    def project(self, bm: BMesh) -> None:
        pass


class EdgeLengthConstraint(Constraint):
    def __init__(self, edge, rest_length: float, weight: float = 1.0) -> None:
        super().__init__(weight)
        self.edge = edge
        self.rest_length = rest_length

    def energy(self):
        v1, v2 = self.edge.verts
        d = (v2.co - v1.co).length
        return (d - self.rest_length) ** 2

    def project(self, bm) -> None:
        v1, v2 = self.edge.verts

        delta = v2.co - v1.co
        d = delta.length

        if d == 0:
            return

        diff = (d - self.rest_length) / 2
        correction = delta.normalized() * diff * self.weight

        v1.co += correction
        v2.co -= correction


class CreaseConstraint(Constraint):
    def __init__(self, crease_edge, weight: float = 1.0) -> None:
        super().__init__(weight)
        self.crease = crease_edge

    def energy(self):
        current = self.crease.compute_dihedral()
        target = math.radians(self.crease.signed_angle())
        return (current - target) ** 2

    def project(self, bm, alpha=0.1) -> None:
        faces = self.crease.get_faces()
        if faces is None:
            return

        flap_face, fixed_face = faces
        v1, v2 = self.crease.edge.verts

        current = self.crease.compute_dihedral()
        target = math.radians(self.crease.signed_angle())

        diff = current - target

        rotate_face_around_edge(flap_face, v1, v2, -alpha * self.weight * diff)
