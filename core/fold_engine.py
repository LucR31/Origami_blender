from .crease_manager import get_valid_creases
from mathutils import Vector
import random
from .constraints import EdgeLengthConstraint, CreaseConstraint
from .collisions import collision_forces_bvh
from .utils import (
    store_original_positions,
    restore_original_positions,
    store_edge_lengths,
    get_edge_lengths,
)


def build_constraints(bm, obj) -> list:
    constraints = []

    # Edge constraints
    edge_lengths = get_edge_lengths(obj)

    for e in bm.edges:
        L = edge_lengths.get(e.index)
        if L is not None:
            constraints.append(EdgeLengthConstraint(e, L))

    # Crease constraints
    creases = get_valid_creases(bm, obj)

    for c in creases:
        constraints.append(CreaseConstraint(c))

    return constraints


def save_original_position(bm, obj) -> None:

    if not getattr(obj, "origami_original_positions", None):
        store_original_positions(bm, obj)

    if not getattr(obj, "origami_edge_lengths", None):
        store_edge_lengths(bm, obj)


def apply_all_folds(bm, obj, iterations: int = 10) -> None:

    save_original_position(bm, obj)
    restore_original_positions(bm, obj)

    # Build constraints
    constraints = build_constraints(bm, obj)

    # Solver loop
    for _ in range(iterations):
        for c in constraints:
            c.project(bm)


def total_energy(constraints):
    return sum(c.energy() for c in constraints if hasattr(c, "energy"))


def solve(bm, obj, iterations: int = 50, alpha: float = 1) -> None:
    """Enery monitoring solver"""

    save_original_position(bm, obj)
    restore_original_positions(bm, obj)
    constraints = build_constraints(bm, obj)

    for _ in range(iterations):

        for c in constraints:
            if isinstance(c, CreaseConstraint):
                c.project(bm, alpha)
            else:
                c.project(bm)

        E = total_energy(constraints)
        print(E)
        if E < 1e-6:
            break


def solve_physics(
    bm,
    obj,
    use_collision: bool,
    threshold: float,
    strength: float,
    steps: int = 50,
    dt: float = 0.1,
) -> None:
    """Physics solver"""

    save_original_position(bm, obj)
    restore_original_positions(bm, obj)
    constraints = build_constraints(bm, obj)

    # init velocities
    velocities = {v: Vector((0, 0, 0)) for v in bm.verts}

    for _ in range(steps):

        forces = {v: Vector((0, 0, 0)) for v in bm.verts}

        # accumulate forces
        for c in constraints:
            f = c.force()
            for v, fv in f.items():
                forces[v] += fv

        # collisions
        if use_collision:
            collision_f = collision_forces_bvh(
                bm, threshold=threshold, strength=strength
            )

            for v in bm.verts:
                forces[v] += collision_f[v]

        # integrate
        for v in bm.verts:
            velocities[v] += forces[v] * dt
            v.co += velocities[v] * dt
