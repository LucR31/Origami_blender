bl_info = {
    "name": "Origami Simulator",
    "author": "Alpha3",
    "version": (0, 1, 0),
    "blender": (4, 1, 0),
    "location": "View3D > Sidebar > Origami",
    "description": "Simulate and interactively fold origami patterns in real-time",
    "category": "Mesh"
}
   

import bpy

from .operators import *
from .core import *

from .properties.crease_props import OrigamiCrease
from .operators.add_crease import ORIGAMI_OT_add_crease
from .operators.reset_op import ORIGAMI_OT_Reset
from .operators.apply_folds import ORIGAMI_OT_apply_folds
from .ui.panel import ORIGAMI_PT_panel

classes = (
    OrigamiCrease,
    ORIGAMI_OT_add_crease,
    ORIGAMI_OT_apply_folds,
    ORIGAMI_OT_Reset,
    ORIGAMI_PT_panel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Object.origami_creases = bpy.props.CollectionProperty(type=OrigamiCrease)
    bpy.types.Object.origami_original_positions = bpy.props.StringProperty()

def unregister():
    del bpy.types.Object.origami_creases
    del bpy.types.Object.origami_original_positions

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)