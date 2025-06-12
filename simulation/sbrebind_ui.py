import bpy


class VIEW3D_PT_sbrebind(bpy.types.Panel):
    bl_label = "Softbody Rebind"
    bl_idname = "VIEW3D_PT_sbrebind"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Blender Tools"

    @classmethod
    def poll(cls, context):
        addon = context.preferences.addons.get("blendertools")
        if addon:
            return addon.preferences.enable_softbody
        else:
            return False

    def draw(self, context):
        layout = self.layout
        layout.operator("blendertools.sbrebindrecursive")


def register():
    print("Registering Softbody Rebind UI")
    bpy.utils.register_class(VIEW3D_PT_sbrebind)


def unregister():
    print("Unregistering Softbody Rebind UI")
    bpy.utils.unregister_class(VIEW3D_PT_sbrebind)
