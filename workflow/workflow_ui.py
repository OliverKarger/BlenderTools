import bpy

class VIEW3D_PT_workflow(bpy.types.Panel):
    bl_label = "Workflow"
    bl_idname = "VIEW3D_PT_workflow"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Blender Tools"

    @classmethod
    def poll(cls, context):
        addon = context.preferences.addons.get("blendertools")
        if addon:
            return addon.preferences.enable_workflow
        else:
            return False


    def draw(self, context):
        pass

def register():
    print("Registering Workflow UI")
    bpy.utils.register_class(VIEW3D_PT_workflow)

def unregister():
    print("Unregistering Workflow UI")
    bpy.utils.unregister_class(VIEW3D_PT_workflow)