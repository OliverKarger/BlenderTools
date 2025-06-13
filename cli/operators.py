import bpy

class BlenderTools_OT_cli_install(bpy.types.Operator):
    bl_idname = "blendertools.cli_install"
    bl_label = "Install CLI"

    def execute(self, context):
        return {"FINISHED"}
    
class BlenderTools_OT_cli_uninstall(bpy.types.Operator):
    bl_idname = "blendertools.cli_uninstall"
    bl_label = "Uninstall CLI"

    def execute(self, context):
        return {"FINISHED"}
    
def register():
    bpy.utils.register_class(BlenderTools_OT_cli_install)
    bpy.utils.register_class(BlenderTools_OT_cli_uninstall)

def unregister():
    bpy.utils.unregister_class(BlenderTools_OT_cli_install)
    bpy.utils.unregister_class(BlenderTools_OT_cli_uninstall)