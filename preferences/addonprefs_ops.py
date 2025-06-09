import bpy

class OT_AddTemplatePath(bpy.types.Operator):
    """ Adds a Template Path from Preferences"""

    bl_idname = "blendertools.add_template_path"
    bl_label = "Add Template Path"

    def execute(self, context):
        prefs = context.preferences.addons["blendertools"].preferences
        prefs.AdditionalImportPaths.add()
        return {'FINISHED'}


class OT_RemoveTemplatePath(bpy.types.Operator):
    """ Removes a Template Path from Preferences"""

    bl_idname = "blendertools.remove_template_path"
    bl_label = "Remove Template Path"

    index: bpy.props.IntProperty()

    def execute(self, context):
        prefs = context.preferences.addons["blendertools"].preferences
        if 0 <= self.index < len(prefs.AdditionalImportPaths):
            prefs.AdditionalImportPaths.remove(self.index)
        return {'FINISHED'}
    
def register():
    bpy.utils.register_class(OT_AddTemplatePath)
    bpy.utils.register_class(OT_RemoveTemplatePath)

def unregister():
    bpy.utils.unregister_class(OT_AddTemplatePath)
    bpy.utils.unregister_class(OT_RemoveTemplatePath)