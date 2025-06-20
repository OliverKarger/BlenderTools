import bpy

from . import armature_sync


class BlenderTools_ArmaturePanel(bpy.types.Panel):
    bl_label = "Armature"
    bl_idname = "BlenderTools_ArmaturePanel"
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

        box.prop(props, "source_armature", icon="ARMATURE_DATA")
        box.prop(props, "target_armature", icon="ARMATURE_DATA")
        box.prop(props, "constraint_mix_mode", icon="CONSTRAINT")

        if props.source_armature and props.target_armature:
            box.separator()

            row = box.row(align=True)
            row.operator(armature_sync.operators.BlenderTools_ArmatureSync_Enum.bl_idname, icon="ARMATURE_DATA")
            row.operator(armature_sync.operators.BlenderTools_ArmatureSync_Check.bl_idname, icon="INFO")

            box.prop(props, "bone_collections", text="Bone Collection")

            box.template_list("BONE_UL_bone_list", "", props, "bones", props, "active_bone_index")

            box.separator()

            row = box.row(align=True)
            row.operator(armature_sync.operators.BlenderTools_ArmatureSync_Enable.bl_idname, icon="LINKED")
            row.operator(armature_sync.operators.BlenderTools_ArmatureSync_Disable.bl_idname, icon="UNLINKED")


def register():
    bpy.utils.register_class(BlenderTools_ArmaturePanel)


def unregister():
    bpy.utils.unregister_class(BlenderTools_ArmaturePanel)
