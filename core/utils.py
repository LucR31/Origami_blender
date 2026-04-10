import json

def store_original_positions(bm, obj) -> None:
    """
    Stores vertex positions as a serialized string in Blender custom props.
    """
    coords = []

    for v in bm.verts:
        coords.append(f"{v.co.x},{v.co.y},{v.co.z}")

    obj["origami_original_positions"] = "|".join(coords)


def store_edge_lengths(bm, obj) -> None:
    """
    Stores edge lengths indexed by edge index.
    """
    data = []

    for e in bm.edges:
        v1, v2 = e.verts
        L = (v2.co - v1.co).length
        data.append(f"{e.index},{L}")

    obj["origami_edge_lengths"] = "|".join(data)


def get_edge_lengths(obj) -> dict:
    """
    Returns:
        {edge_index: length}
    """
    result = {}

    raw = obj.get("origami_edge_lengths", "")
    if not raw:
        return result

    for item in raw.split("|"):
        if not item:
            continue
        idx, L = item.split(",")
        result[int(idx)] = float(L)

    return result


def restore_original_positions(bm, obj) -> None:
    """
    Restores mesh vertices from stored state.
    """
    raw = obj.get("origami_original_positions", "")

    if not raw:
        store_original_positions(bm, obj)
        return

    coords = raw.split("|")

    for v, c in zip(bm.verts, coords):
        x, y, z = map(float, c.split(","))
        v.co.x = x
        v.co.y = y
        v.co.z = z


def store_edge_lengths_json(bm, obj) -> None:
    """
    Cleaner version using JSON (recommended long-term).
    """
    data = []

    for e in bm.edges:
        v1, v2 = e.verts
        L = (v2.co - v1.co).length
        data.append({"edge": e.index, "length": L})

    obj["origami_edge_lengths_json"] = json.dumps(data)


def get_edge_lengths_json(obj) -> dict:
    """
    Safer structured version.
    """
    raw = obj.get("origami_edge_lengths_json", "[]")
    data = json.loads(raw)

    return {item["edge"]: item["length"] for item in data}
