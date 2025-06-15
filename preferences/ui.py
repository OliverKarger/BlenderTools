import bpy

from ..armature import preferences as armature_preferences
from ..camera import preferences as camera_preferences
from ..cli import preferences as cli_preferences
from ..node_groups import preferences as nodegroups_preferences
from ..simulation import preferences as simulation_preferences
from ..utils.icons import IconManager


class BlendertoolsAddonPreferences(bpy.types.AddonPreferences):
    """
    Represents the preferences for the BlenderTools addon.

    This class is used to define and manage the configurable preferences of the BlenderTools addon.
    It allows users to adjust various settings related to different components of the addon, such
    as armature preferences, camera preferences, CLI preferences, node group preferences, and
    simulation preferences. Each category of preferences is managed separately and can be drawn
    in the user interface for interaction.
    """

    # IMPORTANT: This must match the addon folder name
    bl_idname = "blendertools"

    armature: bpy.props.PointerProperty(type=armature_preferences.ArmaturePreferences)
    camera: bpy.props.PointerProperty(type=camera_preferences.CameraPreferences)
    cli: bpy.props.PointerProperty(type=cli_preferences.CliPreferences)
    node_groups: bpy.props.PointerProperty(type=nodegroups_preferences.NodeGroupsPreferences)
    simulation: bpy.props.PointerProperty(type=simulation_preferences.SimulationPreferences)

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        box.label(
            text="A Collection of personal Scripts, combined into a single Addon that i use in my Day-to-Day Work with Blender",  # noqa: E501
            icon_value=IconManager.get_icon_id(),
        )

        self.armature.draw(layout)
        self.camera.draw(layout)
        self.cli.draw(layout)
        self.node_groups.draw(layout)
        self.simulation.draw(layout)


def register():
    bpy.utils.register_class(BlendertoolsAddonPreferences)


def unregister():
    bpy.utils.unregister_class(BlendertoolsAddonPreferences)
