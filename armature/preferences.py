import bpy


class ArmaturePreferences(bpy.types.PropertyGroup):
    """
    Manages preferences for armature tools in Blender.

    This class defines a property group that contains preferences related to
    armature tools. It is used to enable or disable specific functionalities
    within the armature tools panel in Blender. The class also provides a
    method to render a user interface for these preferences. This class is a
    custom extension of Blender's bpy.types.PropertyGroup.
    """

    enabled: bpy.props.BoolProperty(name="Armature Tools enabled", default=True)

    def draw(self, layout):
        box = layout.box()
        box.label(text="Armature Tools", icon="BONE_DATA")
        box.prop(self, "enabled")


def register():
    bpy.utils.register_class(ArmaturePreferences)


def unregister():
    bpy.utils.unregister_class(ArmaturePreferences)
