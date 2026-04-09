def store_original_positions(bm, obj) -> None:
    coords = []
    for v in bm.verts:
        coords.append(f"{v.co.x},{v.co.y},{v.co.z}")

    obj.origami_original_positions = "|".join(coords)


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