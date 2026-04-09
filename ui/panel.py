import bpy

class ORIGAMI_PT_panel(bpy.types.Panel):
    bl_label = "Origami Simulator"
    bl_idname = "ORIGAMI_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Origami"

    def draw(self, context):
        layout = self.layout

        layout.label(text="Fold Tool")
        layout.operator("mesh.origami_fold")