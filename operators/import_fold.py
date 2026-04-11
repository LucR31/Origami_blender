import bpy
import bmesh
import json
from mathutils import Vector


class ORIGAMI_OT_import_fold(bpy.types.Operator):
    bl_idname = "origami.import_fold"
    bl_label = "Import FOLD File"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):

        # LOAD FILE
        with open(self.filepath, "r") as f:
            data = json.load(f)

        verts_2d = data.get("vertices_coords", [])
        edges = data.get("edges_vertices", [])
        assignments = data.get("edges_assignment", [])

        # CREATE MESH
        mesh = bpy.data.meshes.new("OrigamiMesh")
        obj = bpy.data.objects.new("OrigamiObject", mesh)
        context.collection.objects.link(obj)

        bm = bmesh.new()

        bm_verts = []

        for v in verts_2d:
            # lift 2D → 3D (Z = 0)
            bm_verts.append(bm.verts.new(Vector((v[0], v[1], 0))))

        bm.verts.ensure_lookup_table()

        bm_edges = []

        for e in edges:
            v1 = bm_verts[e[0]]
            v2 = bm_verts[e[1]]

            try:
                bm_edges.append(bm.edges.new((v1, v2)))
            except ValueError:
                # edge already exists
                bm_edges.append(bm.edges.get((v1, v2)))

        bm.edges.ensure_lookup_table()

        # CREATE FACES AUTOMATICALLY
        bmesh.ops.contextual_create(bm, geom=bm.edges)
    
        bm.faces.ensure_lookup_table()

        bm.to_mesh(mesh)
        bm.free()

        # CREATE CREASE DATA
        obj.origami_creases.clear()

        for i, e in enumerate(obj.data.edges):

            if i >= len(assignments):
                continue

            a = assignments[i]

            if a not in ("M", "V"):
                continue  # skip boundaries

            c = obj.origami_creases.add()
            c.edge_index = e.index
            c.angle = 0.0

            if a == "M":
                c.crease_type = 'MOUNTAIN'
            else:
                c.crease_type = 'VALLEY'

        self.report({'INFO'}, "FOLD file imported")
        return {'FINISHED'}


    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}