import bpy

from ...utils.viewport_visualizer import draw_objects_wireframe, build_wireframe_batches
from ..utils.camera_view import get_objects_in_camera_view


_runtime_overlay_cache = {}


def draw_callback(context):
    scene = context.scene
    props = scene.blendertools_ifovisualizer

    addon = context.preferences.addons.get("blendertools")
    wire_color = (1.0, 0.0, 0.0, 0.6)
    if addon:
        wire_color = addon.preferences.camera.ifo_visualizer_wire_color

    colliders = [bpy.data.objects.get(entry.name) for entry in props.collider_names]
    colliders = [obj for obj in colliders if obj and obj.visible_get()]

    draw_objects_wireframe(context, colliders, _runtime_overlay_cache, wire_color)


class BlenderTools_IfoVisualizer_Enable(bpy.types.Operator):
    """Enable In-Frame Object Visualization"""

    bl_idname = "blendertools.ifovisualizer_enable"
    bl_label = "Enable In-Frame Object Visualization"

    def execute(self, context):
        scene = context.scene
        props = scene.blendertools_ifovisualizer
        addon = context.preferences.addons.get("blendertools")
        if addon.preferences.settings.viewport_selector_enabled:
            cam = context.active_object
        else:
            cam = props.camera

        if not cam or cam.type != "CAMERA":
            self.report({"ERROR"}, "Active object must be a camera.")
            return {"CANCELLED"}

        visible_objs = [obj for obj in get_objects_in_camera_view(context, cam) if obj.type == "MESH"]

        props.collider_names.clear()
        for obj in visible_objs:
            props.collider_names.add().name = obj.name

        _runtime_overlay_cache.clear()
        build_wireframe_batches(visible_objs, _runtime_overlay_cache)

        if props.overlay_handle and props.overlay_handle != -1:
            try:
                bpy.types.SpaceView3D.draw_handler_remove(props.overlay_handle, "WINDOW")
            except ValueError:
                pass  # Already removed or invalid
            props.overlay_handle = -1

        props.overlay_handle = bpy.types.SpaceView3D.draw_handler_add(draw_callback, (context,), "WINDOW", "POST_VIEW")

        self.report({"INFO"}, f"{len(visible_objs)} object(s) visualized.")
        return {"FINISHED"}


class BlenderTools_IfoVisualizer_Disable(bpy.types.Operator):
    """Disable In-Frame Object Visualization"""

    bl_idname = "blendertools.ifovisualizer_disable"
    bl_label = "Disable In-Frame Object Visualization"

    def execute(self, context):
        props = context.scene.blendertools_ifovisualizer

        try:
            if props.overlay_handle and props.overlay_handle != -1:
                bpy.types.SpaceView3D.draw_handler_remove(props.overlay_handle, "WINDOW")
        except Exception:
            # Handler might already be removed or invalid after undo
            self.report({"WARNING"}, "Invalid Handler")
            pass
        finally:
            props.overlay_handle = -1

        props.collider_names.clear()
        _runtime_overlay_cache.clear()

        self.report({"INFO"}, "In-frame object visualization disabled.")
        return {"FINISHED"}


def register():
    bpy.utils.register_class(BlenderTools_IfoVisualizer_Enable)
    bpy.utils.register_class(BlenderTools_IfoVisualizer_Disable)


def unregister():
    bpy.utils.unregister_class(BlenderTools_IfoVisualizer_Enable)
    bpy.utils.unregister_class(BlenderTools_IfoVisualizer_Disable)
