import bpy


class CameraPreferences(bpy.types.PropertyGroup):
    enabled: bpy.props.BoolProperty(name="Camera Tools enabled", default=True)

    ifo_visualizer_wire_color: bpy.props.FloatVectorProperty(
        name="Visualizer Wire Color",
        subtype="COLOR",  # noqa:F821
        size=4,
        default=(1.0, 0.0, 0.0, 1.0),
        min=0.0,
        max=1.0,  # noqa:F821
    )

    def draw(self, layout):
        box = layout.box()
        box.label(text="Camera Tools", icon="VIEW_CAMERA")
        box.prop(self, "enabled")

        if self.enabled:
            box.prop(self, "ifo_visualizer_wire_color")


def register():
    bpy.utils.register_class(CameraPreferences)


def unregister():
    bpy.utils.unregister_class(CameraPreferences)
