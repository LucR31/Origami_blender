import bpy


class OrigamiCrease(bpy.types.PropertyGroup):
    edge_index: bpy.props.IntProperty()
    angle: bpy.props.FloatProperty(
        name="Angle", default=0.0, min=-180.0, max=180.0, subtype="ANGLE"
    )

    crease_type: bpy.props.EnumProperty(
        items=[
            ("MOUNTAIN", "Mountain", ""),
            ("VALLEY", "Valley", ""),
        ],
        default="VALLEY",
    )
