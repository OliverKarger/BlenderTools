import bpy


class LightsPreferences(bpy.types.PropertyGroup):
    enabled: bpy.props.BoolProperty(name="Light Tools enabled", default=True)

    def draw(self, layout):
        box = layout.box()
        box.label(text="Light Tools", icon="LIGHT")
        box.prop(self, "enabled")


def register():
    bpy.utils.register_class(LightsPreferences)


def unregister():
    bpy.utils.unregister_class(LightsPreferences)
