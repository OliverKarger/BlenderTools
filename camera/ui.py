import bpy

from ..utils.icons import ICON_MAP

from . import ifo_visualizer
from . import ifo_optimizer


class BlenderTools_Camera_HiddenObjectsList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # item = BlenderTools_IfoOptimizerItem
        obj_icon = "OBJECT_DATAMODE"

        obj_icon = ICON_MAP.get(item.object_type, "OBJECT_DATAMODE")

        if self.layout_type in {"DEFAULT", "COMPACT"}:
            layout.label(text=item.name, icon=obj_icon)
        elif self.layout_type == "GRID":
            layout.alignment = "CENTER"
            layout.label(text="", icon=obj_icon)


class BlenderTools_CameraPanel(bpy.types.Panel):
    bl_label = "Camera"
    bl_idname = "BlenderTools_CameraPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Blender Tools"

    @classmethod
    def poll(cls, context):
        addon = context.preferences.addons.get("blendertools")
        return addon and addon.preferences.camera.enabled

    def draw(self, context):
        layout = self.layout
        addon = context.preferences.addons.get("blendertools")
        visualizer_props = context.scene.blendertools_ifovisualizer
        optimizer_props = context.scene.blendertools_ifooptimizer

        box = layout.box()
        box.label(text="IFO Visualizer")
        if not addon.preferences.settings.viewport_selector_enabled:
            box.prop(visualizer_props, "camera", icon="CAMERA_DATA")
        elif context.active_object and context.active_object.type == "CAMERA":
            box.label(text=f"Camera: {context.active_object.name}")

        if visualizer_props.camera or addon.preferences.settings.viewport_selector_enabled:
            box.operator(ifo_visualizer.operators.BlenderTools_IfoVisualizer_Enable.bl_idname, icon="HIDE_OFF")
            box.operator(ifo_visualizer.operators.BlenderTools_IfoVisualizer_Disable.bl_idname, icon="HIDE_ON")

        box = layout.box()
        box.label(text="IFO Optimizer")
        if not addon.preferences.settings.viewport_selector_enabled:
            box.prop(visualizer_props, "camera", icon="CAMERA_DATA")
        elif context.active_object and context.active_object.type == "CAMERA":
            box.label(text=f"Camera: {context.active_object.name}")

        if optimizer_props.camera or addon.preferences.settings.viewport_selector_enabled:
            box.operator(ifo_optimizer.operators.BlenderTools_IfoOptimizer_ShowObjects.bl_idname, icon="HIDE_OFF")
            box.operator(ifo_optimizer.operators.BlenderTools_IfoOptimizer_HideObjects.bl_idname, icon="HIDE_ON")

            box.template_list(
                "BlenderTools_Camera_HiddenObjectsList",
                "",
                optimizer_props,
                "hidden_objects",
                optimizer_props,
                "active_item_index",
            )


def register():
    bpy.utils.register_class(BlenderTools_Camera_HiddenObjectsList)
    bpy.utils.register_class(BlenderTools_CameraPanel)


def unregister():
    bpy.utils.unregister_class(BlenderTools_Camera_HiddenObjectsList)
    bpy.utils.unregister_class(BlenderTools_CameraPanel)
