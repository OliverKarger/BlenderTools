import bpy

from .. import bt_logger
from ...utils.viewport_visualizer import draw_objects_wireframe, build_wireframe_batches

logger = bt_logger.get_logger(__name__)
_runtime_cache = {}  # For GPU batches (cannot store in props)


def get_colliders(context):
    return [obj for obj in context.scene.objects if obj.type == "MESH" and obj.collision and obj.collision.use]


def draw_callback(context):
    props = context.scene.blendertools_collisionvisu

    addon = context.preferences.addons.get("blendertools")
    wire_color = (1.0, 0.0, 0.0, 0.6)
    if addon:
        wire_color = addon.preferences.simulation.collidervisu_wire_color

    colliders = [bpy.data.objects.get(entry.name) for entry in props.collider_names]
    colliders = [obj for obj in colliders if obj and obj.visible_get()]

    draw_objects_wireframe(context, colliders, _runtime_cache, wire_color)


class BlenderTools_CollisionVisualizer_ShowOverlay(bpy.types.Operator):
    bl_idname = "blendertools.collisionvisualizer_showoverlay"
    bl_label = "Show Collider Overlay"

    def execute(self, context):
        props = context.scene.blendertools_collisionvisu

        if props.overlay_handle != -1:
            # Attempt to remove in case it's stale (e.g. after undo)
            try:
                bpy.types.SpaceView3D.draw_handler_remove(props.overlay_handle, "WINDOW")
                logger.info("Stale overlay handler removed.")
            except Exception:
                logger.warning("Overlay handle was already invalid.")
            finally:
                props.overlay_handle = -1

        colliders = get_colliders(context)

        # Store original states
        props.collider_names.clear()
        for obj in colliders:
            props.collider_names.add().name = obj.name
            obj.hide_viewport = False

        _runtime_cache.clear()
        build_wireframe_batches(colliders, _runtime_cache)

        try:
            props.overlay_handle = bpy.types.SpaceView3D.draw_handler_add(
                draw_callback, (context,), "WINDOW", "POST_VIEW"
            )
        except Exception as e:
            logger.error(f"Failed to create draw handler: {e}")
            props.overlay_handle = -1
            return {"CANCELLED"}

        self.report({"INFO"}, f"{len(colliders)} colliders visualized.")
        return {"FINISHED"}


class BlenderTools_CollisionVisualizer_HideOverlay(bpy.types.Operator):
    bl_idname = "blendertools.collisionvisualizer_hideoverlay"
    bl_label = "Hide Collider Overlay"

    def execute(self, context):
        props = context.scene.blendertools_collisionvisu

        if props.overlay_handle != -1:
            try:
                bpy.types.SpaceView3D.draw_handler_remove(props.overlay_handle, "WINDOW")
            except Exception as e:
                logger.warning(f"Failed to remove draw handler: {e}")
            props.overlay_handle = -1

        props.collider_names.clear()
        _runtime_cache.clear()

        self.report({"INFO"}, "Collider overlay cleared.")
        return {"FINISHED"}


def register():
    bpy.utils.register_class(BlenderTools_CollisionVisualizer_ShowOverlay)
    bpy.utils.register_class(BlenderTools_CollisionVisualizer_HideOverlay)


def unregister():
    bpy.utils.unregister_class(BlenderTools_CollisionVisualizer_ShowOverlay)
    bpy.utils.unregister_class(BlenderTools_CollisionVisualizer_HideOverlay)
