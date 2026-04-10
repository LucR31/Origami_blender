import bpy
import bmesh

from ..core.utils import restore_original_positions


class ORIGAMI_OT_Reset(bpy.types.Operator):
    bl_idname = "origami.reset"
    bl_label = "Reset Origami"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = context.object

        if obj is None or obj.mode != "EDIT":
            self.report({"WARNING"}, "Must be in Edit Mode")
            return {"CANCELLED"}

        # Reset crease angles
        for crease in context.object.origami_creases:
            crease.angle = 0.0

        # Restore geometry using core function
        bm = bmesh.from_edit_mesh(obj.data)
        restore_original_positions(bm, obj)
        bmesh.update_edit_mesh(obj.data)

        self.report({"INFO"}, "Origami reset")
        return {"FINISHED"}
