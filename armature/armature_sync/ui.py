import bpy


def view3d_context_menu(self, context):
    """
    Invoke the 3D Viewport context menu for armature-related operations within the Blender environment.
    Provides operators for setting the source and target armatures when the active object is of type
    ARMATURE and the relevant add-on is enabled.

    Parameters:
        self: This instance of the panel invokes the method.
        context: Provides access to Blender's RNA contexts, including required add-on and
            active object information.

    Returns:
        bool: False if the required add-on ("blendertools") is not active. Otherwise, does not
        explicitly return a value.
    """
    addon = context.preferences.addons.get("blendertools")
    if not addon:
        return False

    if not bpy.context.active_object.type == "ARMATURE":
        return

    layout = self.layout

    layout.operator("blendertools.set_armature_source")
    layout.operator("blendertools.set_armature_target")


class BONE_UL_bone_list(bpy.types.UIList):
    """
    Defines a custom UI list class to display and interact with a list of bones.
    This class inherits from `bpy.types.UIList` and provides custom drawing
    behaviors for bone items in the UI.

    The class is designed to handle the display of bones in two layouts:
    'DEFAULT'/'COMPACT' and 'GRID'. It customizes how each bone item appears,
    including properties like synchronization and name display with icons.
    """

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if self.layout_type in {"DEFAULT", "COMPACT"}:
            row = layout.row()

            if item.sync_enabled:
                row.alert = True

            row.prop(item, "should_be_synced", text="")

            row.label(text=item.name, icon="BONE_DATA")

        elif self.layout_type == "GRID":
            layout.alignment = "CENTER"
            layout.label(text="", icon="BONE_DATA")


def register():
    bpy.utils.register_class(BONE_UL_bone_list)

    bpy.types.VIEW3D_MT_object_context_menu.append(view3d_context_menu)


def unregister():
    bpy.utils.unregister_class(BONE_UL_bone_list)

    bpy.types.VIEW3D_MT_object_context_menu.remove(view3d_context_menu)
