from mathutils.bvhtree import BVHTree
from mathutils import Vector


def build_bvh(bm):
    bm.faces.ensure_lookup_table()
    bm.verts.ensure_lookup_table()

    verts = [v.co.copy() for v in bm.verts]
    faces = [[v.index for v in f.verts] for f in bm.faces]

    return BVHTree.FromPolygons(verts, faces)


def collision_forces_bvh(bm, threshold: float = 0.01, strength: float = 0.5):

    forces = {v: Vector((0, 0, 0)) for v in bm.verts}

    bvh = build_bvh(bm)

    for v in bm.verts:

        co = v.co

        location, normal, face_index, distance = bvh.find_nearest(co)

        if location is None:
            continue

        face = bm.faces[face_index]

        if v in face.verts:
            continue

        if distance < threshold:

            direction = co - location

            if direction.length == 0:
                direction = normal
            else:
                direction.normalize()

            penetration = threshold - distance

            force = direction * penetration * strength

            forces[v] += force

    return forces
