import bpy


class VIEW3D_PT_blendertools_armature(bpy.types.Panel):
    """
    Represents the Blender UI Panel for armature tools in Blender Tools add-on.

    This panel provides user interface elements for managing and synchronizing
    armatures in the 3D View editor. It includes options for selecting source and
    target armatures, setting constraint mix modes, enabling or disabling
    synchronization, and a list to display bones with related controls.
    """

    bl_label = "Armature"
    bl_idname = "VIEW3D_PT_blendertools_armature"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Blender Tools"

    @classmethod
    def poll(cls, context):
        addon = context.preferences.addons.get("blendertools")
        return addon and addon.preferences.armature.enabled

    def draw(self, context):
        layout = self.layout
        props = context.scene.blendertools_armaturesync

        box = layout.box()
        box.label(text="Armature Sync")

        box.prop(props, "source_armature")
        box.prop(props, "target_armature")
        box.prop(props, "constraint_mix_mode")

        box.separator()

        row = box.row(align=True)
        row.operator("blendertools.armature_sync_enum", icon="ARMATURE_DATA")
        row.operator("blendertools.armature_sync_check", icon="INFO")

        box.template_list("BONE_UL_bone_list", "", props, "bones", props, "active_bone_index")

        box.separator()

        row = box.row(align=True)
        row.operator("blendertools.armature_sync_enable", icon="LINKED")
        row.operator("blendertools.armature_sync_disable", icon="UNLINKED")


def register():
    bpy.utils.register_class(VIEW3D_PT_blendertools_armature)


def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_blendertools_armature)
