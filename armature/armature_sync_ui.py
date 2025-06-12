import bpy


def view3d_context_menu(self, context):
    addon = context.preferences.addons.get("blendertools")
    if not addon:
        return False

    if not bpy.context.active_object.type == "ARMATURE":
        return

    layout = self.layout

    layout.operator("blendertools.set_armature_source")
    layout.operator("blendertools.set_armature_target")


class BONE_UL_bone_list(bpy.types.UIList):
    def draw_item(
        self, context, layout, data, item, icon, active_data, active_propname, index
    ):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row()

            if item.sync_enabled:
                row.alert = True

            row.prop(item, "should_be_synced", text="")

            row.label(text=item.name, icon='BONE_DATA')

        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text="", icon='BONE_DATA')


class VIEW3D_PT_armature_sync(bpy.types.Panel):
    bl_label = "Armature Sync"
    bl_idname = "VIEW3D_PT_armature_sync"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Blender Tools"

    @classmethod
    def poll(cls, context):
        addon = context.preferences.addons.get("blendertools")
        if addon:
            return addon.preferences.enable_armature
        else:
            return False

    def draw(self, context):
        layout = self.layout
        props = context.scene.blendertools_armaturesync

        layout.label(text="Armature Sync Tools")

        layout.prop(props, "source_armature")
        layout.prop(props, "target_armature")
        layout.prop(props, "constraint_mix_mode")

        layout.separator()

        row = layout.row(align=True)
        row.operator("blendertools.armature_sync_enum", icon='ARMATURE_DATA')
        row.operator("blendertools.armature_sync_check", icon='INFO')

        layout.template_list("BONE_UL_bone_list", "", props, "bones", props, "active_bone_index")

        layout.separator()

        row = layout.row(align=True)
        row.operator("blendertools.armature_sync_enable", icon='LINKED')
        row.operator("blendertools.armature_sync_disable", icon='UNLINKED')


def register():
    print("Registering Armature Sync UI")
    bpy.utils.register_class(BONE_UL_bone_list)
    bpy.utils.register_class(VIEW3D_PT_armature_sync)

    bpy.types.VIEW3D_MT_object_context_menu.append(view3d_context_menu)


def unregister():
    print("Unregistering Armature Sync UI")
    bpy.utils.unregister_class(VIEW3D_PT_armature_sync)
    bpy.utils.unregister_class(BONE_UL_bone_list)

    bpy.types.VIEW3D_MT_object_context_menu.remove(view3d_context_menu)
