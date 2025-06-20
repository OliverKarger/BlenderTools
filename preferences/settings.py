import bpy


class BlenderToolsSettings(bpy.types.PropertyGroup):
    viewport_selector_enabled: bpy.props.BoolProperty(
        name="Viewport Selection",
        description="Use Viewport for Object selection instead of UI Properties",
        default=False,
    )

    def draw(self, layout):
        box = layout.box()
        box.label(text="Global Settings", icon="SCRIPTPLUGINS")
        box.prop(self, "viewport_selector_enabled", icon="VIEW3D")


def register():
    bpy.utils.register_class(BlenderToolsSettings)


def unregister():
    bpy.utils.unregister_class(BlenderToolsSettings)
