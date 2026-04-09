bl_info = {
    "name": "Origami Simulator",
    "author": "L. Fernandez",
    "version": (0, 1, 0),
    "blender": (3, 0, 0),
    "category": "Mesh",
}

import bpy

from .operators.fold import ORIGAMI_OT_fold
from .ui.panel import ORIGAMI_PT_panel

classes = (
    ORIGAMI_OT_fold,
    ORIGAMI_PT_panel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)