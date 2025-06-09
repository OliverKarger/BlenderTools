import bpy
import json
import os

from . import ngtemplates_utils

class NODE_OT_import_node_group_template(bpy.types.Operator):
    """Import Node Group Template from JSON"""
    bl_idname = "blendertools.import_ngtemplate"
    bl_label = "Import Node Group Template"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        if not self.filepath or not os.path.exists(self.filepath):
            self.report({'ERROR'}, "Invalid file path")
            return {'CANCELLED'}

        try:
            with open(self.filepath, 'r') as f:
                data = json.load(f)
        except Exception as e:
            self.report({'ERROR'}, f"Failed to load JSON: {e}")
            return {'CANCELLED'}

        try:
            group_name = bpy.path.clean_name(data.get('name', 'ImportedTemplate'))
            group = bpy.data.node_groups.new(name=group_name, type='ShaderNodeTree')
            group["is_template"] = True

            # Create sockets (default type: Float for inputs, Shader for outputs)
            for name in data['inputs']:
                group.interface.new_socket(name=name, in_out='INPUT', socket_type='NodeSocketFloat')
            for name in data['outputs']:
                group.interface.new_socket(name=name, in_out='OUTPUT', socket_type='NodeSocketShader')

            # Create nodes
            name_to_node = {}
            for node_data in data['nodes']:
                node = group.nodes.new(type=node_data['type'])
                node.name = node_data['name']
                node.location = node_data['location']
                name_to_node[node.name] = node

            # Rebuild internal links only
            for link in data['links']:
                from_node = name_to_node.get(link['from_node'])
                to_node = name_to_node.get(link['to_node'])

                if from_node and to_node:
                    try:
                        from_socket = from_node.outputs[link['from_socket']]
                        to_socket = to_node.inputs[link['to_socket']]
                        group.links.new(from_socket, to_socket)
                    except Exception as e:
                        print(f"Failed to link {from_node.name} → {to_node.name}: {e}")

            self.report({'INFO'}, f"Node group '{group.name}' imported successfully")
            return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, f"Import failed: {e}")
            return {'CANCELLED'}

class NODE_OT_add_ngtemplate_instance_modal(bpy.types.Operator):
    bl_idname = "blendertools.add_node_group_template_modal"
    bl_label = "Insert Node Group Template"
    bl_description = "Choose a TEMPLATE_ node group to insert into the current node tree"
    bl_options = {'REGISTER', 'UNDO'}

    group_name: bpy.props.EnumProperty(
        name="Template",
        description="Select a node group template",
        items=ngtemplates_utils.get_template_node_groups
    )

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=300)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "group_name", text="Template")

    def execute(self, context):
        if self.group_name == "NONE":
            self.report({'ERROR'}, "No valid templates available")
            return {'CANCELLED'}

        space = context.space_data
        group = bpy.data.node_groups.get(self.group_name)

        if not group or not space.edit_tree:
            self.report({'ERROR'}, "Template not found or invalid context")
            return {'CANCELLED'}

        node = space.edit_tree.nodes.new('ShaderNodeGroup')
        node.node_tree = group
        node.location = space.cursor_location

        self.report({'INFO'}, f"Added node group '{self.group_name}'")
        return {'FINISHED'}

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
    
class NODE_OT_export_ngtemplate(bpy.types.Operator):
    """Export Node Group to JSON"""
    bl_idname = "blendertools.export_ngtemplate"
    bl_label = "Export Node Group"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        node = context.active_node
        if not node or node.type != 'GROUP' or not node.node_tree:
            self.report({'ERROR'}, "No valid node group selected")
            return {'CANCELLED'}

        data = ngtemplates_utils.serialize_node_group(node.node_tree)

        with open(f"{self.filepath}.json", 'w') as f:
            json.dump(data, f, indent=4)

        self.report({'INFO'}, f"Node group exported to {self.filepath}")
        return {'FINISHED'}

def register():
    print("Registering Node Group Templates Operators")
    bpy.utils.register_class(NODE_OT_add_ngtemplate_instance)
    bpy.utils.register_class(NODE_OT_export_ngtemplate)
    bpy.utils.register_class(NODE_OT_add_ngtemplate_instance_modal)
    bpy.utils.register_class(NODE_OT_import_node_group_template)


def unregister():
    print("Unregistering Node Group Templates Operators")
    bpy.utils.unregister_class(NODE_OT_add_ngtemplate_instance)
    bpy.utils.unregister_class(NODE_OT_export_ngtemplate)
    bpy.utils.unregister_class(NODE_OT_add_ngtemplate_instance_modal)
    bpy.utils.unregister_class(NODE_OT_import_node_group_template)
