import bpy


class OT_AddTemplatePath(bpy.types.Operator):
    bl_idname = "blendertools.add_template_path"
    bl_label = "Add Template Path"

    def execute(self, context):
        prefs = context.preferences.addons["blendertools"].preferences
        prefs.additional_import_paths.add()
        return {'FINISHED'}


class OT_RemoveTemplatePath(bpy.types.Operator):
    bl_idname = "blendertools.remove_template_path"
    bl_label = "Remove Template Path"

    index = bpy.props.IntProperty()

    def execute(self, context):
        prefs = context.preferences.addons["blendertools"].preferences
        if 0 <= self.index < len(prefs.additional_import_paths):
            prefs.additional_import_paths.remove(self.index)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(OT_AddTemplatePath)
    bpy.utils.register_class(OT_RemoveTemplatePath)


def unregister():
    bpy.utils.unregister_class(OT_AddTemplatePath)
    bpy.utils.unregister_class(OT_RemoveTemplatePath)
