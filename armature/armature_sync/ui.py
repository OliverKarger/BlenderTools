import bpy

from . import operators


def view3d_context_menu(self, context):
    addon = context.preferences.addons.get("blendertools")
    if not addon:
        return False

    if not bpy.context.active_object.type == "ARMATURE":
        return

    layout = self.layout

    layout.operator(operators.BlenderTools_ArmatureSync_SetSource.bl_idname, icon="ARMATURE_DATA")
    layout.operator(operators.BlenderTools_ArmatureSync_SetTarget.bl_idname, icon="ARMATURE_DATA")


class BONE_UL_bone_list(bpy.types.UIList):
    def filter_items(self, context, data, propname):
        props = context.scene.blendertools_armaturesync
        collection_filter = props.bone_collections

        items = getattr(data, propname)
        flt_flags = []
        flt_neworder = []

        for item in items:
            if collection_filter == "ALL" or item.bone_group == collection_filter:
                flt_flags.append(self.bitflag_filter_item)
            else:
                flt_flags.append(0)  # filtered out

        return flt_flags, flt_neworder

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if self.layout_type in {"DEFAULT", "COMPACT"}:
            row = layout.row()

            if item.sync_enabled:
                row.alert = True

            row.prop(item, "should_be_synced", text="")

            row.label(text=item.name, icon="BONE_DATA")
            if item.bone_group:
                row.label(text=item.bone_group, icon="OUTLINER_COLLECTION")

        elif self.layout_type == "GRID":
            layout.alignment = "CENTER"
            layout.label(text="", icon="BONE_DATA")


def register():
    bpy.utils.register_class(BONE_UL_bone_list)
    bpy.types.VIEW3D_MT_object_context_menu.append(view3d_context_menu)


def unregister():
    bpy.utils.unregister_class(BONE_UL_bone_list)
    bpy.types.VIEW3D_MT_object_context_menu.remove(view3d_context_menu)
