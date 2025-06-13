import bpy
import sys
import os

from ..cli import utils as cli_utils


class BlenderTools_OT_AddTemplatePath(bpy.types.Operator):
    bl_idname = "blendertools.add_template_path"
    bl_label = "Add Template Path"

    def execute(self, context):
        prefs = context.preferences.addons["blendertools"].preferences
        prefs.additional_import_paths.add()
        return {"FINISHED"}


class BlenderTools_OT_RemoveTemplatePath(bpy.types.Operator):
    bl_idname = "blendertools.remove_template_path"
    bl_label = "Remove Template Path"

    index = bpy.props.IntProperty()

    def execute(self, context):
        prefs = context.preferences.addons["blendertools"].preferences
        if 0 <= self.index < len(prefs.additional_import_paths):
            prefs.additional_import_paths.remove(self.index)
        return {"FINISHED"}


class BlenderTools_OT_InstallWrapperScript(bpy.types.Operator):
    bl_idname = "blendertools.install_wrapper_script"
    bl_label = "Install Wrapper Script"

    def execute(self, context):
        cli_utils.install.install_wrapper()
        return {"FINISHED"}


class BlenderTools_OT_UninstallWrapperScript(bpy.types.Operator):
    bl_idname = "blendertools.uninstall_wrapper_script"
    bl_label = "Uninstall Wrapper Script"

    def execute(self, context):
        cli_utils.install.uninstall_wrapper()
        return {"FINISHED"}


def register():
    bpy.utils.register_class(BlenderTools_OT_AddTemplatePath)
    bpy.utils.register_class(BlenderTools_OT_RemoveTemplatePath)
    bpy.utils.register_class(BlenderTools_OT_InstallWrapperScript)
    bpy.utils.register_class(BlenderTools_OT_UninstallWrapperScript)


def unregister():
    bpy.utils.unregister_class(BlenderTools_OT_AddTemplatePath)
    bpy.utils.unregister_class(BlenderTools_OT_RemoveTemplatePath)
    bpy.utils.unregister_class(BlenderTools_OT_InstallWrapperScript)
    bpy.utils.unregister_class(BlenderTools_OT_UninstallWrapperScript)
