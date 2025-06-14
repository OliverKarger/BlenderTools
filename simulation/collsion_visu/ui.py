import bpy


class VIEW3D_PT_collisionvisu(bpy.types.Panel):
    bl_label = "Collision Visualizer"
    bl_idname = "VIEW3D_PT_collisionvisu"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Blender Tools"

    @classmethod
    def poll(cls, context):
        addon = context.preferences.addons.get("blendertools")
        if addon:
            return addon.preferences.enable_simulation
        else:
            return False

    def draw(self, context):
        layout = self.layout
        layout.operator("blendertools.show_collider_overlay")
        layout.operator("blendertools.hide_collider_overlay")


def register():
    bpy.utils.register_class(VIEW3D_PT_collisionvisu)


def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_collisionvisu)
