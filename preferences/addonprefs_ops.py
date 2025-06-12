import bpy
import sys
import os

class BlenderTools_OT_install_cli(bpy.types.Operator):
    bl_idname = "blendertools.install_cli"
    bl_label = "Install 'blender-cli' command"
    bl_description = "Installs a wrapper to run the BlenderTools CLI from terminal as 'blender-cli'"

    def execute(self, context):
        cli_command = f"{sys.executable} -m cli"

        # Detect platform-specific location
        if sys.platform == "win32":
            target_dir = os.path.join(os.getenv("APPDATA"), "BlenderTools")
            script_path = os.path.join(target_dir, "blender-cli.bat")
            script_content = f"@echo off\n\"{sys.executable}\" -m cli %*"
        else:
            target_dir = os.path.expanduser("~/.local/bin")
            script_path = os.path.join(target_dir, "blender-cli")
            script_content = f"#!/bin/sh\n\"{sys.executable}\" -m cli \"$@\""

        os.makedirs(target_dir, exist_ok=True)

        with open(script_path, "w") as f:
            f.write(script_content)

        if sys.platform != "win32":
            st = os.stat(script_path)
            os.chmod(script_path, st.st_mode | stat.S_IEXEC)

        self.report({'INFO'}, f"'blender-cli' installed at: {script_path}")
        return {'FINISHED'}


class BLENDERTOOLS_OT_uninstall_cli(bpy.types.Operator):
    bl_idname = "blendertools.uninstall_cli"
    bl_label = "Uninstall 'blender-cli' command"
    bl_description = "Removes the 'blender-cli' command-line wrapper installed earlier"

    def execute(self, context):
        if sys.platform == "win32":
            target_dir = os.path.join(os.getenv("APPDATA"), "BlenderTools")
            script_path = os.path.join(target_dir, "blender-cli.bat")
        else:
            target_dir = os.path.expanduser("~/.local/bin")
            script_path = os.path.join(target_dir, "blender-cli")

        if os.path.exists(script_path):
            try:
                os.remove(script_path)
                self.report({'INFO'}, f"'blender-cli' removed from: {script_path}")
            except Exception as e:
                self.report({'ERROR'}, f"Failed to remove: {str(e)}")
                return {'CANCELLED'}
        else:
            self.report({'WARNING'}, f"'blender-cli' not found at: {script_path}")

        return {'FINISHED'}


class BlenderTools_OT_AddTemplatePath(bpy.types.Operator):
    bl_idname = "blendertools.add_template_path"
    bl_label = "Add Template Path"

    def execute(self, context):
        prefs = context.preferences.addons["blendertools"].preferences
        prefs.additional_import_paths.add()
        return {'FINISHED'}


class BlenderTools_OT_RemoveTemplatePath(bpy.types.Operator):
    bl_idname = "blendertools.remove_template_path"
    bl_label = "Remove Template Path"

    index = bpy.props.IntProperty()

    def execute(self, context):
        prefs = context.preferences.addons["blendertools"].preferences
        if 0 <= self.index < len(prefs.additional_import_paths):
            prefs.additional_import_paths.remove(self.index)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(BlenderTools_OT_AddTemplatePath)
    bpy.utils.register_class(BlenderTools_OT_RemoveTemplatePath)
    bpy.utils.register_class(BlenderTools_OT_install_cli)
    bpy.utils.register_class(BLENDERTOOLS_OT_uninstall_cli)


def unregister():
    bpy.utils.unregister_class(BlenderTools_OT_AddTemplatePath)
    bpy.utils.unregister_class(BlenderTools_OT_RemoveTemplatePath)
    bpy.utils.unregister_class(BlenderTools_OT_install_cli)   
    bpy.utils.unregister_class(BLENDERTOOLS_OT_uninstall_cli)
