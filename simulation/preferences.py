import bpy


class SimulationPreferences(bpy.types.PropertyGroup):
    """
    Represents the preferences for simulation tools.

    This class defines the properties and settings related to the simulation tools
    in Blender. It acts as a container for configurable options and visual
    preferences used within the simulation tools. The settings can be adjusted via
    the UI and integrate seamlessly into Blender's property group system.
    """

    enabled: bpy.props.BoolProperty(name="Simulation Tools enabled", default=True)

    collidervisu_wire_color: bpy.props.FloatVectorProperty(
        name="Visualizer Wire Color",
        subtype="COLOR",  # noqa:F821
        size=4,
        default=(0.0, 1.0, 0.0, 1.0),
        min=0.0,
        max=1.0,  # noqa:F821
    )

    def draw(self, layout):
        box = layout.box()
        box.label(text="Simulation Tools", icon="PHYSICS")
        box.prop(self, "enabled")

        if self.enabled:
            box.prop(self, "collidervisu_wire_color")


def register():
    bpy.utils.register_class(SimulationPreferences)


def unregister():
    bpy.utils.unregister_class(SimulationPreferences)
