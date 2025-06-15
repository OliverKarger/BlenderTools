import bpy
from . import utils as cli_utils


class BlenderTools_OT_InstallWrapperScript(bpy.types.Operator):
    """
    Handles the installation of the wrapper script for Blender tools.

    This class represents a Blender Operator that invokes a utility function to
    install a wrapper script. It acts as an interface for Blender users to trigger
    the installation process directly from the Blender interface.
    """

    bl_idname = "blendertools.install_wrapper_script"
    bl_label = "Install Wrapper Script"

    def execute(self, context):
        cli_utils.install.install_wrapper()
        return {"FINISHED"}


class BlenderTools_OT_UninstallWrapperScript(bpy.types.Operator):
    """
    Provides functionality to uninstall a wrapper script via a Blender operator.

    This class is an implementation of a Blender operator. It provides a mechanism
    to uninstall a wrapper script using an external utility function. This operator
    executes the uninstall process and finalizes the operation.
    """

    bl_idname = "blendertools.uninstall_wrapper_script"
    bl_label = "Uninstall Wrapper Script"

    def execute(self, context):
        cli_utils.install.uninstall_wrapper()
        return {"FINISHED"}


class CliPreferences(bpy.types.PropertyGroup):
    """
    Represents CLI preferences for the Blender tools add-on.

    This class defines the CLI-specific preferences used in the Blender
    tools add-on. It provides a user interface for managing CLI-related
    operations like installing and uninstalling wrapper scripts.
    """

    def draw(self, layout):
        box = layout.box()
        box.label(text="CLI", icon="CONSOLE")
        box.operator("blendertools.install_wrapper_script")
        box.operator("blendertools.uninstall_wrapper_script")


def register():
    bpy.utils.register_class(BlenderTools_OT_InstallWrapperScript)
    bpy.utils.register_class(BlenderTools_OT_UninstallWrapperScript)
    bpy.utils.register_class(CliPreferences)


def unregister():
    bpy.utils.unregister_class(BlenderTools_OT_InstallWrapperScript)
    bpy.utils.unregister_class(BlenderTools_OT_UninstallWrapperScript)
    bpy.utils.unregister_class(CliPreferences)
