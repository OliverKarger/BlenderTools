import bpy

from . import cone_mesh


class BlenderTools_LightToolsPanel(bpy.types.Panel):
    bl_label = "Lights"
    bl_idname = "BlenderTools_LightToolsPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Blender Tools"

    def draw(self, context):
        layout = self.layout
        addon = context.preferences.addons.get("blendertools")
        conemesh_props = context.scene.blendertools_lightconemesh

        box = layout.box()
        box.label(text="Cone Mesh Generator")
        if not addon.preferences.settings.viewport_selector_enabled:
            box.prop(conemesh_props, "light", icon="LIGHT")
        if conemesh_props.light or addon.preferences.settings.viewport_selector_enabled:
            box.operator(cone_mesh.operators.BlenderTools_LightVolume_Create.bl_idname, icon="MESH_DATA")


def register():
    bpy.utils.register_class(BlenderTools_LightToolsPanel)


def unregister():
    bpy.utils.unregister_class(BlenderTools_LightToolsPanel)
