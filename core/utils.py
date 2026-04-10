def store_original_positions(bm, obj) -> None:
    coords = []
    for v in bm.verts:
        coords.append(f"{v.co.x},{v.co.y},{v.co.z}")

    obj.origami_original_positions = "|".join(coords)


def store_edge_lengths(bm, obj) -> None:
    data = []
    for e in bm.edges:
        v1, v2 = e.verts
        L = (v2.co - v1.co).length
        data.append(f"{e.index},{L}")

    obj.origami_edge_lengths = "|".join(data)


def get_edge_lengths(obj) -> dict:
    result = {}

    if not obj.origami_edge_lengths:
        return result

    for item in obj.origami_edge_lengths.split("|"):
        idx, L = item.split(",")
        result[int(idx)] = float(L)

    return result


def restore_original_positions(bm, obj) -> None:
    if not obj.origami_original_positions:
        store_original_positions(bm, obj)
        return

    coords = obj.origami_original_positions.split("|")

    for v, c in zip(bm.verts, coords):
        x, y, z = map(float, c.split(","))
        v.co.x = x
        v.co.y = y
        v.co.z = z
