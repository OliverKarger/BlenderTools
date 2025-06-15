import bpy


class NODE_PT_blendertools_nodegroups(bpy.types.Panel):
    """
    Represents a Blender UI panel in the Node Editor for managing node group templates.

    This class defines a custom UI panel that appears in the "Node Editor" space under the
    "Blender Tools" category. It provides tools for exporting node groups, importing JSON
    node group templates, and adding node group templates.
    """

    bl_space_type = "NODE_EDITOR"
    bl_Region_type = "UI"
    bl_category = "Blender Tools"
    bl_label = "Node Group Templates"
    bl_region_type = "UI"

    @classmethod
    def poll(cls, context):
        addon = context.preferences.addons.get("blendertools")
        return addon and addon.preferences.node_groups.enabled

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        node = context.active_node

        if node and node.type == "GROUP":
            col.label(text=f"Selected: {node.name}")
            col.operator("blendertools.export_ngtemplate", text="Export to JSON")
        else:
            col.label(text="Select a Node Group", icon="INFO")

        layout.operator("blendertools.add_node_group_template_modal")
        layout.operator("blendertools.import_ngtemplate")


def register():
    bpy.utils.register_class(NODE_PT_blendertools_nodegroups)


def unregister():
    bpy.utils.unregister_class(NODE_PT_blendertools_nodegroups)
