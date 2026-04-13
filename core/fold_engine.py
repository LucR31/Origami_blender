from .crease_manager import get_valid_creases
import random
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

def save_original_position(bm, obj) -> None:

    if not getattr(obj, "origami_original_positions", None):
        store_original_positions(bm, obj)

    if not getattr(obj, "origami_edge_lengths", None):
        store_edge_lengths(bm, obj)

# Main fucntion
def apply_all_folds(bm, obj, iterations: int = 10):

    save_original_position(bm, obj)
    restore_original_positions(bm, obj)

    # Build constraints
    constraints = build_constraints(bm, obj)

    # Solver loop
    for _ in range(iterations):
        for c in constraints:
            c.project(bm)

def total_energy(constraints):
    return sum(
        c.energy() for c in constraints
        if hasattr(c, "energy")
    )

def solve(bm, obj, iterations=50, alpha=1):
    """ Enery monitoring solver """

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
