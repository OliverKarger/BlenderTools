import bpy


class CameraPreferences(bpy.types.PropertyGroup):
    """
    Represents camera preferences shared across tools in Blender.

    This class manages properties related to camera tools, such as the
    overall enable/disable state and visual preferences like the color
    used for wireframe visualizers. It is designed to be used as a
    property group in Blender, allowing for easy integration into user
    interface panels and other features.
    """

    enabled: bpy.props.BoolProperty(name="Armature Tools enabled", default=True)

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
