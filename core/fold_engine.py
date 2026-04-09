import math
from mathutils import Matrix

def fold_mesh(bm, angle):
    selected_edges = [e for e in bm.edges if e.select]

    if len(selected_edges) != 1:
        return False

    edge = selected_edges[0]
    v1, v2 = edge.verts

    axis = (v2.co - v1.co).normalized()
    pivot = v1.co

    # Pick one face as seed
    if not edge.link_faces:
        return False

    start_face = edge.link_faces[0]

    # BFS to get one side
    faces_to_rotate = set()
    stack = [start_face]

    while stack:
        f = stack.pop()
        if f in faces_to_rotate:
            continue

        faces_to_rotate.add(f)

        for e in f.edges:
            if e == edge:
                continue

            for linked_face in e.link_faces:
                if linked_face not in faces_to_rotate:
                    stack.append(linked_face)

    # Collect vertices
    verts_to_rotate = set()
    for f in faces_to_rotate:
        for v in f.verts:
            verts_to_rotate.add(v)

    # Rotation
    rot = Matrix.Rotation(
        math.radians(angle),
        3,
        axis
    )

    for v in verts_to_rotate:
        v.co = rot @ (v.co - pivot) + pivot

    return True