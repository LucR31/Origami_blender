import bpy
import bmesh
from ..core.fold_engine import apply_all_folds, solve, solve_physics
from ..core.utils import (
    ensure_shape_keys,
    store_folded_shape,
    restore_basis,
    animate_shape_key
)


class ORIGAMI_OT_apply_folds(bpy.types.Operator):
    bl_idname = "mesh.origami_apply_folds"
    bl_label = "Apply All Folds"

    def execute(self, context):
        obj = context.object
        me = obj.data

        # Sim params
        iterations = context.scene.origami_iterations
        mode = context.scene.origami_solver_mode

        # Collision params
        use_collision = context.scene.origami_use_collision
        strength = context.scene.origami_collision_strength
        threshold = context.scene.origami_collision_threshold

        # Animation
        animate = context.scene.origami_animate

        if animate:
            bm = bmesh.new()
            bm.from_mesh(me)
            bm.verts.ensure_lookup_table()
            bm.edges.ensure_lookup_table()
            bm.faces.ensure_lookup_table()
            ensure_shape_keys(obj)
        else:
            bm = bmesh.from_edit_mesh(me)

        # Main loop
        if mode == "PROJECTION":
            apply_all_folds(bm, obj, iterations=iterations)

        elif mode == "ENERGY":
            solve(bm, obj, iterations=iterations)

        elif mode == "PHYSICS":
            solve_physics(
                bm,
                obj,
                use_collision=use_collision,
                strength=strength,
                threshold=threshold,
                steps=iterations,
            )

        if animate:
            store_folded_shape(obj, bm)
            #bm.to_mesh(me)
            restore_basis(obj)
            animate_shape_key(obj)
            bm.free()

        else:
            bmesh.update_edit_mesh(me)

        return {"FINISHED"}
