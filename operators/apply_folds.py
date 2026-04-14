import bpy
import bmesh
from ..core.fold_engine import apply_all_folds, solve, solve_physics


class ORIGAMI_OT_apply_folds(bpy.types.Operator):
    bl_idname = "mesh.origami_apply_folds"
    bl_label = "Apply All Folds"

    def execute(self, context):
        obj = context.object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)

        # Sim params
        iterations = context.scene.origami_iterations
        mode = context.scene.origami_solver_mode

        # Collision params
        use_collision = context.scene.origami_use_collision
        strength = context.scene.origami_collision_strength
        threshold = context.scene.origami_collision_threshold

        # Animation
        if context.scene.origami_animate:
            pass

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

        bmesh.update_edit_mesh(me)
        return {"FINISHED"}
