import bpy

from ..armature import preferences as armature_preferences
from ..camera import preferences as camera_preferences
from ..cli import preferences as cli_preferences
from ..simulation import preferences as simulation_preferences
from ..lights import preferences as light_preferences
from ..utils.icons import IconManager
from . import settings


class BlendertoolsAddonPreferences(bpy.types.AddonPreferences):
    # IMPORTANT: This must match the addon folder name
    bl_idname = "blendertools"

    settings: bpy.props.PointerProperty(type=settings.BlenderToolsSettings)
    armature: bpy.props.PointerProperty(type=armature_preferences.ArmaturePreferences)
    camera: bpy.props.PointerProperty(type=camera_preferences.CameraPreferences)
    cli: bpy.props.PointerProperty(type=cli_preferences.CliPreferences)
    simulation: bpy.props.PointerProperty(type=simulation_preferences.SimulationPreferences)
    lights: bpy.props.PointerProperty(type=light_preferences.LightsPreferences)

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        box.label(
            text="A Collection of personal Scripts, combined into a single Addon that i use in my Day-to-Day Work with Blender",  # noqa: E501
            icon_value=IconManager.get_icon_id(),
        )

        self.settings.draw(layout)
        self.armature.draw(layout)
        self.camera.draw(layout)
        self.cli.draw(layout)
        self.simulation.draw(layout)
        self.lights.draw(layout)


def register():
    bpy.utils.register_class(BlendertoolsAddonPreferences)


def unregister():
    bpy.utils.unregister_class(BlendertoolsAddonPreferences)
