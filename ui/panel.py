import bpy


class ORIGAMI_PT_panel(bpy.types.Panel):
    bl_label = "Origami Editor"
    bl_idname = "ORIGAMI_PT_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Origami"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene

        layout.prop(scene, "origami_solver_mode")
        layout.operator("mesh.origami_add_crease")
        layout.operator("mesh.origami_apply_folds")
        layout.prop(scene, "origami_iterations")
        layout.operator("origami.reset", icon="LOOP_BACK")
        layout.operator("origami.import_fold")

        layout.label(text="Animation")
        layout.prop(scene, "origami_animate")
        layout.prop(scene, "origami_frame_step")

        layout.label(text="Collision")
        layout.prop(scene, "origami_use_collision")

        col = layout.column()
        col.enabled = scene.origami_use_collision
        col.prop(scene, "origami_collision_strength")
        col.prop(scene, "origami_collision_threshold")
        if not scene.origami_use_collision:
            layout.label(text="⚠ Collisions disabled", icon='ERROR')

        layout.separator()

        for i, crease in enumerate(obj.origami_creases):
            box = layout.box()
            box.label(text=f"Crease {i}")

            box.prop(crease, "angle", slider=False)
            box.prop(crease, "crease_type")
