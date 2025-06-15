import bpy

from .. import bt_logger
from ...utils.viewport_visualizer import draw_objects_wireframe

logger = bt_logger.get_logger(__name__)

_overlay_data = {
    "handle": None,
    "colliders": [],
    "wire_states": {},
    "colors": {},
    "display_types": {},
    "hide_viewport": {},
}


def get_colliders(context):
    """
    Generate a list of mesh objects with enabled collision in the provided scene context.

    This function iterates over all objects in the scene of the given context and filters
    those that are of type "MESH" and have collision enabled. Collision is considered enabled
    if both the `collision` attribute and the `collision.use` attribute of the object are true.

    Parameters:
        context (Context): The scene context containing all objects to be filtered.

    Returns:
        list: A list of objects from the scene that meet the collision and type criteria.
    """
    return [obj for obj in context.scene.objects if obj.collision and obj.collision.use and obj.type == "MESH"]


def draw_callback(context):
    """
    Draws the wireframe overlay for simulation colliders using specified context and wire color.

    Checks if the 'blendertools' addon is enabled in the user's preferences. If enabled, it retrieves
    the wire color for collider visualization from the addon's preferences. Otherwise, a default red
    wire color is used. Utilizes the `draw_objects_wireframe` function to render the wireframe for the
    objects listed in the `_overlay_data["colliders"]` variable.
    """
    addon = context.preferences.addons.get("blendertools")
    wire_color = (1.0, 0.0, 0.0, 0.6)
    if addon:
        wire_color = addon.preferences.simulation.collidervisu_wire_color

    draw_objects_wireframe(context, _overlay_data["colliders"], wire_color)


class BlenderTools_ShowColliderOverlay(bpy.types.Operator):
    """Operator to show a collider overlay in the Blender viewport.

    This operator allows users to highlight and visualize colliders in the Blender
    viewport by enabling specific overlay settings. It ensures that all colliders
    are temporarily unhidden and customized with wireframe and color properties
    for better visibility during the operation. The operator maintains and restores
    the original visibility and display settings after modifications.
    """

    bl_idname = "blendertools.show_collider_overlay"
    bl_label = "Show Collider Overlay"

    def execute(self, context):
        if _overlay_data["handle"] is not None:
            self.report({"WARNING"}, "Overlay already active.")
            return {"CANCELLED"}

        _overlay_data["colliders"] = get_colliders(context)
        _overlay_data["wire_states"] = {obj.name: obj.show_wire for obj in _overlay_data["colliders"]}
        _overlay_data["colors"] = {obj.name: tuple(obj.color) for obj in _overlay_data["colliders"]}
        _overlay_data["display_types"] = {obj.name: obj.display_type for obj in _overlay_data["colliders"]}
        _overlay_data["hide_viewport"] = {obj.name: obj.hide_viewport for obj in _overlay_data["colliders"]}

        for obj in _overlay_data["colliders"]:
            obj.hide_viewport = False  # Temporarily unhide to draw
            logger.debug(f"Overlay: highlighting {obj.name}")

        _overlay_data["handle"] = bpy.types.SpaceView3D.draw_handler_add(
            draw_callback, (context,), "WINDOW", "POST_VIEW"
        )

        return {"FINISHED"}


class BlenderTools_HideColliderOverlay(bpy.types.Operator):
    """
    Operator to hide the collider overlay in Blender.

    This class provides functionality to manage and remove the collider overlay, including
    the restoration of object properties like wireframe display, viewport visibility, colors,
    and display types to their original states. It also removes the draw handler associated
    with the overlay and clears the cache data stored for the colliders.
    """

    bl_idname = "blendertools.hide_collider_overlay"
    bl_label = "Hide Collider Overlay"

    def execute(self, context):
        for obj in _overlay_data["colliders"]:
            if obj.name in _overlay_data["wire_states"]:
                obj.show_wire = _overlay_data["wire_states"][obj.name]
            if obj.name in _overlay_data["colors"]:
                obj.color = _overlay_data["colors"][obj.name]
            if obj.name in _overlay_data["display_types"]:
                obj.display_type = _overlay_data["display_types"][obj.name]
            if obj.name in _overlay_data["hide_viewport"]:
                obj.hide_viewport = _overlay_data["hide_viewport"][obj.name]

        if _overlay_data["handle"]:
            bpy.types.SpaceView3D.draw_handler_remove(_overlay_data["handle"], "WINDOW")
            _overlay_data["handle"] = None

        _overlay_data["colliders"].clear()
        _overlay_data["wire_states"].clear()
        _overlay_data["colors"].clear()
        _overlay_data["display_types"].clear()
        _overlay_data["hide_viewport"].clear()

        logger.debug("Overlay cleared.")
        return {"FINISHED"}


def register():
    bpy.utils.register_class(BlenderTools_ShowColliderOverlay)
    bpy.utils.register_class(BlenderTools_HideColliderOverlay)


def unregister():
    bpy.utils.unregister_class(BlenderTools_ShowColliderOverlay)
    bpy.utils.unregister_class(BlenderTools_HideColliderOverlay)
