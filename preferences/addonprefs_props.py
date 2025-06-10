import bpy

class TemplatePathItem(bpy.types.PropertyGroup):
    """ Item for Blender Template Path in Preferences """

    path: bpy.props.StringProperty(
        name="Path",
        description="Additional path to scan for node group templates",
        subtype='DIR_PATH'
    )

def register():
    bpy.utils.register_class(TemplatePathItem)

def unregister():
    bpy.utils.unregister_class(TemplatePathItem)