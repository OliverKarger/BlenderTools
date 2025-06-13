import bpy

class BlenderTools_OT_octane_light_converter_panel(bpy.types.Panel):

    bl_idname = "blendertools.octane_light_converter_panel"
    bl_label = "Octane Converter"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "data"

    @classmethod
    def poll(cls, context):
        addon = context.preferences.addons.get("blendertools")
        if addon:
            return addon.preferences.enable_node_groups and context.light is not None
        else:
            return False

    def draw(self, context):
        layout = self.layout
        layout.operator("blendertools.convert_lightsource_to_octane")
        pass


def register():
    bpy.utils.register_class(BlenderTools_OT_octane_light_converter_panel)

def unregister():
    bpy.utils.unregister_class(BlenderTools_OT_octane_light_converter_panel)