import bpy

class NODE_OT_add_ngtemplate_instance(bpy.types.Operator):
    bl_idname = "blendertools.add_node_group_instance"
    bl_label = "Add Node Group Template"
    bl_options = {'REGISTER', 'UNDO'}

    group_name: bpy.props.StringProperty(name="Node Group Name")

    def execute(self, context):
        space = context.space_data
        if not space.edit_tree or not self.group_name:
            return {'CANCELLED'}

        group = bpy.data.node_groups.get(self.group_name)
        if not group:
            return {'CANCELLED'}

        node = space.edit_tree.nodes.new('ShaderNodeGroup')
        node.node_tree = group
        node.location = context.space_data.cursor_location

        return {'FINISHED'}
    
def register():
    print("Registering Node Group Templates Operators")
    bpy.utils.register_class(NODE_OT_add_ngtemplate_instance)

def unregister():
    print("Unregistering Node Group Templates Operators")
    bpy.utils.unregister_class(NODE_OT_add_ngtemplate_instance)