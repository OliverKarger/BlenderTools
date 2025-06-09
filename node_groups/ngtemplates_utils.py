import bpy

def serialize_node_group(group):
    # Correctly extract inputs and outputs from interface
    inputs = [item for item in group.interface.items_tree if item.item_type == 'SOCKET' and item.in_out == 'INPUT']
    outputs = [item for item in group.interface.items_tree if item.item_type == 'SOCKET' and item.in_out == 'OUTPUT']

    data = {
        'name': group.name,
        'inputs': [item.name for item in inputs],
        'outputs': [item.name for item in outputs],
        'nodes': [],
        'links': []
    }

    for node in group.nodes:
        data['nodes'].append({
            'name': node.name,
            'type': node.bl_idname,
            'location': list(node.location),
            'inputs': [sock.name for sock in node.inputs],
            'outputs': [sock.name for sock in node.outputs]
        })

    for link in group.links:
        data['links'].append({
            'from_node': link.from_node.name,
            'from_socket': link.from_socket.name,
            'to_node': link.to_node.name,
            'to_socket': link.to_socket.name
        })

    return data

def get_template_node_groups(self, context):
    return [
        (group.name, group.name, "")
        for group in bpy.data.node_groups
        if group.bl_idname == 'ShaderNodeTree' and group.name.startswith("TEMPLATE_")
    ] or [("NONE", "No templates found", "")]