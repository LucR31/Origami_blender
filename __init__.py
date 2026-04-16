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
    ORIGAMI_OT_import_fold,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Object.origami_creases = bpy.props.CollectionProperty(type=OrigamiCrease)
    bpy.types.Object.origami_original_positions = bpy.props.StringProperty()
    bpy.types.Scene.origami_iterations = bpy.props.IntProperty(
        name="Iterations", default=50, min=1, max=500
    )
    bpy.types.Scene.origami_solver_mode = bpy.props.EnumProperty(
        name="Solver",
        items=[
            ("PROJECTION", "Projection", ""),
            ("ENERGY", "Energy", ""),
            ("PHYSICS", "Physics", ""),
        ],
        default="PROJECTION",
    )
    bpy.types.Scene.origami_animate = bpy.props.BoolProperty(
        name="Animate", default=False
    )

    bpy.types.Scene.origami_frame_step = bpy.props.IntProperty(
        name="Frame Step", default=1, min=1, max=10
    )
    bpy.types.Scene.origami_use_collision = bpy.props.BoolProperty(
        name="Use Collision", description="Enable self-collision handling", default=True
    )

    bpy.types.Scene.origami_collision_strength = bpy.props.FloatProperty(
        name="Collision Strength",
        description="Repulsion force for collisions",
        default=0.5,
        min=0.0,
        max=10.0,
    )

    bpy.types.Scene.origami_collision_threshold = bpy.props.FloatProperty(
        name="Collision Distance",
        description="Minimum allowed distance between surfaces",
        default=0.01,
        min=0.0001,
        max=0.1,
    )


def unregister():
    del bpy.types.Object.origami_creases
    del bpy.types.Object.origami_original_positions
    del bpy.types.Scene.origami_iterations
    del bpy.types.Scene.origami_solver_mode
    del bpy.types.Scene.origami_animate
    del bpy.types.Scene.origami_frame_step
    del bpy.types.Scene.origami_use_collision
    del bpy.types.Scene.origami_collision_strength
    del bpy.types.Scene.origami_collision_threshold

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
