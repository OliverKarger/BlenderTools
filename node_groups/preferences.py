import bpy


class TemplatePathItem(bpy.types.PropertyGroup):
    """
    Represents a path item within a template.

    This class is used to handle and store a directory path in Blender's
    property group system. It is primarily utilized to manage template paths
    that are associated with various functionalities in Blender.
    """

    path: bpy.props.StringProperty(name="Path", subtype="DIR_PATH")  # noqa:F821


class BlenderTools_OT_AddNodeGroupTemplatePath(bpy.types.Operator):
    """
    Represents an operator for adding a new template path for node groups in
    Blender.

    This class integrates with Blender's API to allow users to add a new template
    path for node groups to the addon's preferences. It extends the Blender's
    Operator class and is intended for use with the 'blendertools' addon.
    """

    bl_idname = "blendertools.add_nodegroup_template_path"
    bl_label = "Add Template Path"

    def execute(self, context):
        prefs = context.preferences.addons["blendertools"].preferences
        prefs.node_groups.additional_import_paths.add()
        return {"FINISHED"}


class BlenderTools_OT_RemoveNodeGroupTemplatePath(bpy.types.Operator):
    """
    Operator to remove a node group template path.

    This operator is used to remove a specified node group template path
    from the additional import paths in the Blender preferences. The
    operation will only proceed if the provided index is within the
    valid range of available paths.
    """

    bl_idname = "blendertools.remove_nodegroup_template_path"
    bl_label = "Remove Template Path"

    index: bpy.props.IntProperty(name="Path Index")

    def execute(self, context):
        prefs = context.preferences.addons["blendertools"].preferences
        if 0 <= self.index < len(prefs.node_groups.additional_import_paths):
            prefs.node_groups.additional_import_paths.remove(self.index)
        return {"FINISHED"}


class NodeGroupsPreferences(bpy.types.PropertyGroup):
    """
    Stores and manages preferences for node group tools in Blender.

    This class defines properties and user interface elements for managing preferences
    related to using node groups. It includes options to enable or disable the node
    group tools, control the auto-import feature, and manage additional import paths.
    These preferences are displayed within a dedicated UI interface in Blender.
    """

    enabled: bpy.props.BoolProperty(name="Node Group Tools enabled", default=True)

    auto_import_enabled: bpy.props.BoolProperty(name="Auto Import enabled", default=True)

    additional_import_paths: bpy.props.CollectionProperty(name="Additional Paths", type=TemplatePathItem)

    def draw(self, layout):
        box = layout.box()
        box.label(text="Node Group Tools", icon="NODE")
        box.prop(self, "enabled")

        if self.enabled:
            box.prop(self, "auto_import_enabled")

            path_box = box.box()
            path_box.label(text="Additional Import Paths", icon="FILE_FOLDER")
            path_box.operator("blendertools.add_nodegroup_template_path")

            for idx, item in enumerate(self.additional_import_paths):
                row = path_box.row()
                row.prop(item, "path", text=f"Path {idx + 1}")
                op = row.operator("blendertools.remove_nodegroup_template_path")
                op.index = idx


def register():
    bpy.utils.register_class(BlenderTools_OT_AddNodeGroupTemplatePath)
    bpy.utils.register_class(BlenderTools_OT_RemoveNodeGroupTemplatePath)
    bpy.utils.register_class(TemplatePathItem)
    bpy.utils.register_class(NodeGroupsPreferences)


def unregister():
    bpy.utils.unregister_class(NodeGroupsPreferences)
    bpy.utils.unregister_class(TemplatePathItem)
    bpy.utils.unregister_class(BlenderTools_OT_AddNodeGroupTemplatePath)
    bpy.utils.unregister_class(BlenderTools_OT_RemoveNodeGroupTemplatePath)
