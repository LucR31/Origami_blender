bl_info = {
    "name": "Origami Simulator",
    "author": "Alpha3",
    "version": (0, 1, 0),
    "blender": (4, 1, 0),
    "location": "View3D > Sidebar > Origami",
    "description": "Simulate and interactively fold origami patterns in real-time",
    "category": "Mesh",
}


import bpy

from .operators import *
from .core import *

from .properties.crease_props import OrigamiCrease
from .operators.add_crease import ORIGAMI_OT_add_crease
from .operators.reset_op import ORIGAMI_OT_Reset
from .operators.apply_folds import ORIGAMI_OT_apply_folds
from .ui.panel import ORIGAMI_PT_panel
from .operators.import_fold import ORIGAMI_OT_import_fold

classes = (
    OrigamiCrease,
    ORIGAMI_OT_add_crease,
    ORIGAMI_OT_apply_folds,
    ORIGAMI_OT_Reset,
    ORIGAMI_PT_panel,
    ORIGAMI_OT_import_fold
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Object.origami_creases = bpy.props.CollectionProperty(type=OrigamiCrease)
    bpy.types.Object.origami_original_positions = bpy.props.StringProperty()
    bpy.types.Scene.origami_iterations = bpy.props.IntProperty(
        name="Iterations",
        default=50,
        min=1,
        max=500
    )


def unregister():
    del bpy.types.Object.origami_creases
    del bpy.types.Object.origami_original_positions
    del bpy.types.Scene.origami_iterations

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
