import bpy
import bmesh
from ..core.fold_engine import apply_all_folds, apply_all_constraints

class ORIGAMI_OT_apply_folds(bpy.types.Operator):
    bl_idname = "mesh.origami_apply_folds"
    bl_label = "Apply All Folds"

    def execute(self, context):
        obj = context.object
        me = obj.data

        bm = bmesh.from_edit_mesh(me)

        apply_all_constraints(bm, obj)

        bmesh.update_edit_mesh(me)
        return {'FINISHED'}