import bpy
import bmesh
from ..core.fold_engine import fold_mesh

class ORIGAMI_OT_fold(bpy.types.Operator):
    bl_idname = "mesh.origami_fold"
    bl_label = "Fold Origami"
    bl_options = {'REGISTER', 'UNDO'}

    angle = bpy.props.FloatProperty(name="Angle",default=45.0)

    def execute(self, context):
        obj = context.object
        me = obj.data

        bm = bmesh.from_edit_mesh(me)

        result = fold_mesh(bm, self.angle)

        if not result:
            self.report({'ERROR'}, "Fold failed")
            return {'CANCELLED'}

        bmesh.update_edit_mesh(me)
        return {'FINISHED'}