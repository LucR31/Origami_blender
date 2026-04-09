import bpy
from ..core.fold_engine import update_folds_callback

class OrigamiCrease(bpy.types.PropertyGroup):
    def angle_update(self, context):
        update_folds_callback(context)
    edge_index: bpy.props.IntProperty()
    angle: bpy.props.FloatProperty(
        name="Angle",
        default=0.0,
        min=-180.0,
        max=180.0,
        subtype='ANGLE',
        #update=angle_update  # <- callback on slider change
    )

    crease_type: bpy.props.EnumProperty(
        items=[
            ('MOUNTAIN', "Mountain", ""),
            ('VALLEY', "Valley", ""),
        ],
        default='VALLEY',
        #update=angle_update  # also update instantly when type changes
    )