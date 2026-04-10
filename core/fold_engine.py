from .crease_manager import get_valid_creases
from .constraints import EdgeLengthConstraint, CreaseConstraint
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


# Main fucntion
def apply_all_folds(bm, obj, iterations: int = 10):

    # Init
    if not getattr(obj, "origami_original_positions", None):
        store_original_positions(bm, obj)

    if not getattr(obj, "origami_edge_lengths", None):
        store_edge_lengths(bm, obj)

    # Reset
    restore_original_positions(bm, obj)

    # Build constraints
    constraints = build_constraints(bm, obj)

    # Solver loop
    for _ in range(iterations):
        for constraint in constraints:
            constraint.project(bm)
