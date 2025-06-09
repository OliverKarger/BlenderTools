import bpy

class NODE_MT_ngtemplates_menu(bpy.types.Menu):
    bl_label = "Blender Tools Templates"
    bl_idname = "NODE_MT_ngtemplates_menu"

    def draw(self, context):
        layout = self.layout

        # List node groups tagged with a specific prefix, for example
        for group in bpy.data.node_groups:
            if group.bl_idname == 'ShaderNodeTree' and group.name.startswith("TEMPLATE_"):
                op = layout.operator("node.add_node_group_instance", text=group.name)
                op.group_name = group.name

def menu_func(self, context):
    layout = self.layout
    layout.separator()
    layout.menu("NODE_MT_ngtemplates_menu", text="Blender Tools Templates")

def register():
    print("Registering Node Group Templates UI")
    bpy.utils.register_class(NODE_MT_ngtemplates_menu)
    bpy.types.NODE_MT_context_menu.append(menu_func)

def unregister():
    print("Unregistering Node Group Templates UI")
    bpy.types.NODE_MT_context_menu.remove(menu_func)
    bpy.utils.unregister_class(NODE_MT_ngtemplates_menu)