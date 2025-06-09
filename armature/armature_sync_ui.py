import bpy

class BONE_UL_bone_list(bpy.types.UIList):
     def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.label(text=item.Name)

class VIEW3D_PT_armature_sync(bpy.types.Panel):
    bl_label = "Armature Sync"
    bl_idname = "VIEW3D_PT_armature_sync"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Blender Tools"

    def draw(self, context):
        layout = self.layout
        props = context.scene.blendertools_armaturesync

        layout.label(text="Armature Sync Tools")

        layout.prop(props, "SourceArmature")
        layout.prop(props, "TargetArmature")

        layout.separator()

        row = layout.row(align=True)
        row.operator("blendertools.armature_sync_enum", icon='ARMATURE_DATA')
        row.operator("blendertools.armature_sync_check", icon='INFO')

        layout.template_list("BONE_UL_bone_list", "", props, "Bones", props, "ActiveBoneIndex")

        layout.separator()

        row = layout.row(align=True)
        row.operator("blendertools.armature_sync_enable", icon='LINKED')
        row.operator("blendertools.armature_sync_disable", icon='UNLINKED')

def register():
    print("Registering Armature Sync UI")
    bpy.utils.register_class(BONE_UL_bone_list)
    bpy.utils.register_class(VIEW3D_PT_armature_sync)

def unregister():
    print("Unregistering Armature Sync UI")
    bpy.utils.unregister_class(VIEW3D_PT_armature_sync)
    bpy.utils.unregister_class(BONE_UL_bone_list)