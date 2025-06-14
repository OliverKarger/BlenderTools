import bpy
import gpu
from gpu_extras.batch import batch_for_shader

from .. import bt_logger

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
    return [obj for obj in context.scene.objects if obj.collision and obj.collision.use and obj.type == "MESH"]


def draw_callback(context):
    wire_color = (1.0, 0.0, 0.0, 0.6)
    addon = context.preferences.addons.get("blendertools")
    if addon:
        wire_color = addon.preferences.collidervisu_wire_color

    shader = gpu.shader.from_builtin("UNIFORM_COLOR")
    shader.bind()
    shader.uniform_float("color", wire_color)  # Red-ish

    for obj in _overlay_data["colliders"]:
        if not obj.visible_get():
            continue

        mesh = obj.to_mesh()
        if not mesh:
            continue

        verts = [obj.matrix_world @ v.co for v in mesh.vertices]
        edges = [(e.vertices[0], e.vertices[1]) for e in mesh.edges]

        batch = batch_for_shader(shader, "LINES", {"pos": verts}, indices=edges)
        batch.draw(shader)
        obj.to_mesh_clear()


class BlenderTools_ShowColliderOverlay(bpy.types.Operator):
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
            obj.show_wire = True
            obj.show_all_edges = True
            obj.display_type = "WIRE"
            obj.color = (1.0, 0.2, 0.2, 1.0)
            logger.debug(f"Overlay: highlighting {obj.name}")

        _overlay_data["handle"] = bpy.types.SpaceView3D.draw_handler_add(
            draw_callback, (context,), "WINDOW", "POST_VIEW"
        )

        return {"FINISHED"}


class BlenderTools_HideColliderOverlay(bpy.types.Operator):
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
