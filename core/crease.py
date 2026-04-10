from bmesh.types import BMEdge, BMFace
from dataclasses import dataclass
from typing import Optional, List
from .edge_utils import compute_dihedral_angle


@dataclass
class CreaseEdge:
    edge: BMEdge
    angle: float
    crease_type: str

    def signed_angle(self) -> float:
        """Return angle with mountain/valley sign"""
        if self.crease_type == "MOUNTAIN":
            return -self.angle
        return self.angle

    def get_faces(self) -> Optional[List[BMFace]]:
        """
        Return the face/s that should rotate around this edge.
        Assumes exactly two faces per crease edge, skips otherwise.
        """
        if len(self.edge.link_faces) != 2:
            return None

        f1, f2 = self.edge.link_faces
        return [f1, f2]

    def compute_dihedral(self) -> float:
        """
        Returns angle between the normals of the two adjacent planes
        """
        faces = self.get_faces()
        if faces is None:
            return 0.0

        f1, f2 = faces
        v1, v2 = self.edge.verts

        return compute_dihedral_angle(v1, v2, f1, f2)
