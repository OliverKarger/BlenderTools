import bpy


class ArmaturePreferences(bpy.types.PropertyGroup):
    enabled: bpy.props.BoolProperty(name="Armature Tools enabled", default=True)

    def draw(self, layout):
        box = layout.box()
        box.label(text="Armature Tools", icon="BONE_DATA")
        box.prop(self, "enabled")


def register():
    bpy.utils.register_class(ArmaturePreferences)


def unregister():
    bpy.utils.unregister_class(ArmaturePreferences)
