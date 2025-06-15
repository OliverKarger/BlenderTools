import bpy
import mathutils
from bpy_extras.object_utils import world_to_camera_view

from ...utils.viewport_visualizer import draw_objects_wireframe

_overlay_data = {
    "handle": None,
    "colliders": [],
    "wire_states": {},
    "colors": {},
    "display_types": {},
    "hide_viewport": {},
}


def draw_callback(context):
    """
    Draws the wireframe for certain objects in the Blender viewport using a specified color.

    The function retrieves the wireframe color for the visualizer from the add-on preferences
    if available. Otherwise, it defaults to a specific red wireframe color. The wireframe is
    drawn for the objects specified in the "_overlay_data" collection.

    Args:
        context (bpy.types.Context): Blender context providing access to the current state
        within Blender, including data and preferences.
    """
    addon = context.preferences.addons.get("blendertools")
    wire_color = (1.0, 0.0, 0.0, 0.6)
    if addon:
        wire_color = addon.preferences.camera.ifo_visualizer_wire_color

    draw_objects_wireframe(context, _overlay_data["colliders"], wire_color)


def get_objects_in_camera_view(context, camera):
    """
    Determines the objects that are visible within the camera's view in the given context.

    This function evaluates all objects in the scene to check if they are meshes and
    visible in the camera's view by projecting their bounding box corners into the
    camera's coordinate space. It uses the evaluated dependency graph for accurate
    object transformations during runtime.

    Parameters:
        context: bpy.types.Context
            The current Blender context, which contains information about the scene,
            viewport, and other relevant data.
        camera: bpy.types.Object
            The camera object to evaluate object visibility from.

    Returns:
        list[bpy.types.Object]
            A list of objects that are visible within the provided camera's field
            of view.
    """
    scene = context.scene
    depsgraph = context.evaluated_depsgraph_get()
    visible = []

    for obj in scene.objects:
        if obj.type != "MESH" or not obj.visible_get():
            continue

        ob_eval = obj.evaluated_get(depsgraph)
        corners = [ob_eval.matrix_world @ mathutils.Vector(c) for c in ob_eval.bound_box]

        if any(
            0.0 <= (co := world_to_camera_view(scene, camera, corner)).x <= 1.0 and 0.0 <= co.y <= 1.0 and co.z >= 0.0
            for corner in corners
        ):
            visible.append(obj)

    return visible


class BlenderTools_Ifo_Visualizer_Enable(bpy.types.Operator):
    """
    Operator class for enabling in-frame object visualization in Blender.

    This operator is used to enable the visualization of objects visible within the
    camera's field of view by adding a draw handler in the 3D Viewport. It ensures
    that the active object is a camera and collects the objects that are within the
    camera view. The visualized objects are then rendered as an overlay using a
    custom draw callback.
    """

    bl_idname = "blendertools.ifo_visualizer_enable"
    bl_label = "Enable In-Frame Object Visualization"

    def execute(self, context):
        cam = context.object
        if not cam or cam.type != "CAMERA":
            self.report({"ERROR"}, "Active object must be a camera.")
            return {"CANCELLED"}

        _overlay_data["colliders"] = get_objects_in_camera_view(context, cam)

        if _overlay_data["handle"] is None:
            _overlay_data["handle"] = bpy.types.SpaceView3D.draw_handler_add(
                draw_callback, (context,), "WINDOW", "POST_VIEW"
            )
            self.report({"INFO"}, f"{len(_overlay_data['colliders'])} object(s) visualized.")

        return {"FINISHED"}


class BlenderTools_Ifo_Visualizer_Disable(bpy.types.Operator):
    """
    Operator to disable the in-frame object visualization in Blender.

    This operator is part of the Blender Tools add-on and is used to
    disable the overlay visualization of in-frame objects within the
    3D view. It clears the overlay data and removes the associated
    draw handler, effectively stopping the visualization. This can
    be useful when the visualization is no longer needed and you
    want to clean up the display.
    """

    bl_idname = "blendertools.ifo_visualizer_disable"
    bl_label = "Disable In-Frame Object Visualization"

    def execute(self, context):
        if _overlay_data["handle"] is not None:
            bpy.types.SpaceView3D.draw_handler_remove(_overlay_data["handle"], "WINDOW")
            _overlay_data["handle"] = None

        _overlay_data["colliders"].clear()
        self.report({"INFO"}, "In-frame object visualization disabled.")
        return {"FINISHED"}


def register():
    bpy.utils.register_class(BlenderTools_Ifo_Visualizer_Enable)
    bpy.utils.register_class(BlenderTools_Ifo_Visualizer_Disable)


def unregister():
    bpy.utils.unregister_class(BlenderTools_Ifo_Visualizer_Enable)
    bpy.utils.unregister_class(BlenderTools_Ifo_Visualizer_Disable)
