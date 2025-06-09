import bpy

from . import ngtemplates_menus

class NODE_PT_ngtemplates_panel(bpy.types.Panel):
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Blender Tools'
    bl_label = "Node Templates"

    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'ShaderNodeTree'

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        node = context.active_node

        if node and node.type == 'GROUP':
            col.label(text=f"Selected: {node.name}")
            col.operator("blendertools.export_ngtemplate", text="Export to JSON")
        else:
            col.label(text="Select a Node Group", icon='INFO')

        layout.operator("blendertools.add_node_group_template_modal")
        layout.operator("blendertools.import_ngtemplate")

def register():
    print("Registering Node Group Templates UI")
    bpy.utils.register_class(NODE_PT_ngtemplates_panel)
    bpy.types.NODE_MT_context_menu.append(ngtemplates_menus.templates_menu)

def unregister():
    print("Unregistering Node Group Templates UI")
    bpy.types.NODE_MT_context_menu.remove(ngtemplates_menus.templates_menu)
    bpy.utils.unregister_class(NODE_PT_ngtemplates_panel)