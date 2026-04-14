import bpy
import bmesh
import json
from mathutils import Vector


class ORIGAMI_OT_import_fold(bpy.types.Operator):
    bl_idname = "origami.import_fold"
    bl_label = "Import FOLD File"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):

        # Load data
        with open(self.filepath, "r") as f:
            data = json.load(f)

        verts_2d = data.get("vertices_coords", [])
        edges_data = data.get("edges_vertices", [])
        assignments = data.get("edges_assignment", [])
        faces_data = data.get("faces_vertices", [])
        face_orders = data.get("faceOrders", [])
        edges_angle = data.get("edges_foldAngle", [])

        # Create mesh
        mesh = bpy.data.meshes.new("OrigamiMesh")
        obj = bpy.data.objects.new("OrigamiObject", mesh)
        context.collection.objects.link(obj)

        bm = bmesh.new()

        # Create vertices
        bm_verts = []

        for v in verts_2d:
            bm_verts.append(bm.verts.new(Vector((v[0], v[1], 0))))

        bm.verts.ensure_lookup_table()

        # Create edges
        for e in edges_data:
            v1, v2 = bm_verts[e[0]], bm_verts[e[1]]

            try:
                bm.edges.new((v1, v2))
            except ValueError:
                pass  # edge already exists

        bm.edges.ensure_lookup_table()

        # Create faces
        if faces_data:
            for f in faces_data:
                verts = [bm_verts[i] for i in f]
                try:
                    bm.faces.new(verts)
                except ValueError:
                    pass
        else:
            # Auto
            bmesh.ops.contextual_create(bm, geom=bm.edges)

        bm.faces.ensure_lookup_table()

        # Finalize mesh
        bm.to_mesh(mesh)
        bm.free()

        # Store face orders (for future solver use)
        obj["origami_face_orders"] = json.dumps(face_orders)

        # Assignment map (M or V)
        edge_map = {}

        for i, e in enumerate(edges_data):

            if i >= len(assignments):
                continue

            a = assignments[i]
            angle = edges_angle[i]

            if a not in ("M", "V"):
                continue

            v1, v2 = e
            key = tuple(sorted((v1, v2)))

            edge_map[key] = (a, angle)

        # Create crease data
        obj.origami_creases.clear()
        mesh = obj.data

        for e in mesh.edges:

            v1 = e.vertices[0]
            v2 = e.vertices[1]

            key = tuple(sorted((v1, v2)))

            if key not in edge_map:
                continue

            a, angle = edge_map[key]

            c = obj.origami_creases.add()
            c.edge_index = e.index
            c.angle = angle

            if a == "M":
                c.crease_type = "MOUNTAIN"
            else:
                c.crease_type = "VALLEY"

        # DEBUG INFO (VERY USEFUL)
        print("FOLD IMPORT:")
        print("Verts:", len(obj.data.vertices))
        print("Edges:", len(obj.data.edges))
        print("Faces:", len(obj.data.polygons))
        print("Creases:", len(obj.origami_creases))
        print("FaceOrders:", len(face_orders))

        self.report({"INFO"}, "FOLD file imported successfully")
        return {"FINISHED"}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}
