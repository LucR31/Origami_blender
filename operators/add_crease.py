import bpy
import bmesh


class ORIGAMI_OT_add_crease(bpy.types.Operator):
    bl_idname = "mesh.origami_add_crease"
    bl_label = "Add Crease"

    def execute(self, context):
        obj = context.object
        bm = bmesh.from_edit_mesh(obj.data)

        selected_edges = [e for e in bm.edges if e.select]

        if len(selected_edges) != 1:
            self.report({"ERROR"}, "Select exactly one edge")
            return {"CANCELLED"}

        edge = selected_edges[0]

        crease = obj.origami_creases.add()
        crease.edge_index = edge.index
        crease.angle = 0.0

        self.report({"INFO"}, "Crease added")
        return {"FINISHED"}
