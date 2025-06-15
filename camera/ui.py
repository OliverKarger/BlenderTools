import bpy


class VIEW3D_PT_blendertools_camera(bpy.types.Panel):
    """
    Represents the Camera panel within the 3D View UI in Blender.

    This class defines a custom user interface panel for cameras in Blender,
    displayed in the "Blender Tools" category of the 3D View sidebar. It provides
    tools specific to camera management and visualization within a Blender scene.
    It ensures functionality is enabled based on the add-on preferences and
    context of the current object.
    """

    bl_label = "Camera"
    bl_idname = "VIEW3D_PT_blendertools_camera"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Blender Tools"

    @classmethod
    def poll(cls, context):
        addon = context.preferences.addons.get("blendertools")
        return addon and addon.preferences.camera.enabled

    def draw(self, context):
        layout = self.layout
        if bpy.context.object and bpy.context.object.type == "CAMERA":
            box = layout.box()
            box.label(text="IFO Visualizer")
            box.operator("blendertools.ifo_visualizer_enable")
            box.operator("blendertools.ifo_visualizer_disable")


def register():
    bpy.utils.register_class(VIEW3D_PT_blendertools_camera)


def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_blendertools_camera)
