from core.constraints import EdgeLengthConstraint
from mathutils import Vector
from .framework import test


@test(group="constrains")
def test_edge_length_restoration():

    v1 = Vector((0, 0, 0))
    v2 = Vector((2, 0, 0))

    edge = type("E", (), {"verts": (v1, v2)})

    constraint = EdgeLengthConstraint(edge, 1.0)
    constraint.project(None)

    midpoint = (v1 + v2) / 2

    assert abs((v2 - v1).length - 1.0) < 1e-6
    assert abs(midpoint.x - 1.0) < 1e-6

@test(group="test")
def fake_test():
    return True