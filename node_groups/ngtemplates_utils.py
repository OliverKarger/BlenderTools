import bpy

def serialize_node_group(group):
    # Tag the node group as a template
    group["is_template"] = True

    inputs = [
        item.name for item in group.interface.items_tree
        if item.item_type == 'SOCKET' and item.in_out == 'INPUT'
    ]
    outputs = [
        item.name for item in group.interface.items_tree
        if item.item_type == 'SOCKET' and item.in_out == 'OUTPUT'
    ]

    node_names = {node.name for node in group.nodes}

    data = {
        'name': group.name,
        'inputs': inputs,
        'outputs': outputs,
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
        if link.from_node.name in node_names and link.to_node.name in node_names:
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
        if group.bl_idname == 'ShaderNodeTree' and group.get("is_template", False)
    ] or [("NONE", "No templates found", "")]