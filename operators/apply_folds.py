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
        iterations = context.scene.origami_iterations
        mode = context.scene.origami_solver_mode

        if mode == "PROJECTION":
            apply_all_folds(bm, obj)

        elif mode == "ENERGY":
            solve(bm, obj, iterations=iterations)

        elif mode == "PHYSICS":
            solve_physics(bm, obj, steps=iterations)

        bmesh.update_edit_mesh(me)
        return {"FINISHED"}
