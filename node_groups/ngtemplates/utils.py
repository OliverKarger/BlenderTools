import bpy
import json
import os


def serialize_node_group(group):
    """
    Serializes a node group into a dictionary representation.

    This function processes a node group and extracts its relevant attributes
    along with its inputs, outputs, nodes, and links. The resulting dictionary
    representation provides a structured summary of the node group for external
    usage, ensuring each element of the group is comprehensively captured.
    """
    # Tag the node group as a template
    group["is_template"] = True

    inputs = [item.name for item in group.interface.items_tree if item.item_type == "SOCKET" and item.in_out == "INPUT"]
    outputs = [
        item.name for item in group.interface.items_tree if item.item_type == "SOCKET" and item.in_out == "OUTPUT"
    ]

    node_names = {node.name for node in group.nodes}

    data = {"name": group.name, "inputs": inputs, "outputs": outputs, "nodes": [], "links": []}

    for node in group.nodes:
        data["nodes"].append(
            {
                "name": node.name,
                "type": node.bl_idname,
                "location": list(node.location),
                "inputs": [sock.name for sock in node.inputs],
                "outputs": [sock.name for sock in node.outputs],
            }
        )

    for link in group.links:
        if link.from_node.name in node_names and link.to_node.name in node_names:
            data["links"].append(
                {
                    "from_node": link.from_node.name,
                    "from_socket": link.from_socket.name,
                    "to_node": link.to_node.name,
                    "to_socket": link.to_socket.name,
                }
            )

    return data


def get_template_node_groups(self, context):
    """
    Gets the list of template node groups from Blender's node groups.

    The function filters node groups in Blender that are of type 'ShaderNodeTree' and
    have the custom property 'is_template' set to True. It returns a list of tuples
    containing the name of the group as both the identifier and label. If no such
    node groups are found, a default single entry indicating no templates are found
    is returned.

    Parameters:
        context: Any
            The context in which the function is executed. It is not
            directly used but is part of the method signature due to
            Blender API conventions.

    Returns:
        list[tuple[str, str, str]]
            A list of tuples where each tuple contains the following:
            - The identifier of the node group.
            - The label of the node group.
            - An empty description string.
    """
    return [
        (group.name, group.name, "")
        for group in bpy.data.node_groups
        if group.bl_idname == "ShaderNodeTree" and group.get("is_template", False)
    ] or [("NONE", "No templates found", "")]


def import_template_from_file(filepath):
    """
    Imports a template from a JSON file and creates a corresponding node group in Blender.

    This function reads a specified JSON file containing template data for a node group,
    creates a new ShaderNodeTree node group in Blender's data structure, and initializes
    its inputs, outputs, and node connections based on the file's content. The function ensures
    unique naming for the node group and nodes. Any broken links in the template will be
    skipped and logged as messages.

    Parameters:
        filepath (str): The path to the JSON file containing template data.

    Raises:
        FileNotFoundError: If the specified file does not exist or cannot be opened.
        json.JSONDecodeError: If the JSON file contains invalid JSON content.

    Notes:
        - The JSON file is expected to have a specific structure, including keys for
          "inputs", "outputs", "nodes", and "links".
        - Socket types are assumed to be "NodeSocketFloat" for inputs and
          "NodeSocketShader" for outputs unless specified otherwise in the template.
        - If a node group with the specified name already exists, a "_copy" suffix is
          added to the new name to ensure uniqueness.
    """
    with open(filepath, "r") as f:
        data = json.load(f)

    group_name = bpy.path.clean_name(data.get("name", "ImportedTemplate"))
    if group_name in bpy.data.node_groups:
        group_name = f"{group_name}_copy"

    group = bpy.data.node_groups.new(name=group_name, type="ShaderNodeTree")
    group["is_template"] = True

    for name in data["inputs"]:
        group.interface.new_socket(name=name, in_out="INPUT", socket_type="NodeSocketFloat")
    for name in data["outputs"]:
        group.interface.new_socket(name=name, in_out="OUTPUT", socket_type="NodeSocketShader")

    name_to_node = {}
    for node_data in data["nodes"]:
        node = group.nodes.new(type=node_data["type"])
        node.name = node_data["name"]
        node.location = node_data["location"]
        name_to_node[node.name] = node

    for link in data["links"]:
        from_node = name_to_node.get(link["from_node"])
        to_node = name_to_node.get(link["to_node"])
        if from_node and to_node:
            try:
                from_socket = from_node.outputs[link["from_socket"]]
                to_socket = to_node.inputs[link["to_socket"]]
                group.links.new(from_socket, to_socket)
            except Exception as e:
                print(f"Skipping broken link: {e}")


def auto_import_templates():
    """
    Auto-imports templates for the Blendertools add-on.

    This function checks if the Blendertools add-on is enabled and then
    retrieves user preferences to determine whether auto-import is enabled.
    If auto-import is enabled, it resolves template directories from the
    default location and any additional user-defined paths. Templates found
    in these directories that match the `.json` extension are imported using
    the `import_template_from_file` function.

    Raises exceptions if a template file fails to import and logs all
    processing activities to the system console.

    Returns
    -------
    None
        Returns None if the add-on is not enabled or auto-import is
        disabled. Also serves as the termination for the timer used for this
        process.

    Parameters
    ----------
    None
    """
    addon = bpy.context.preferences.addons.get("blendertools")
    if not addon:
        return None

    prefs = addon.preferences
    if not prefs.auto_import_enabled:
        return None

    # Resolve default path relative to addon dir
    addon_dir = os.path.dirname(__file__)
    default_path = os.path.join(addon_dir, "templates")

    search_paths = [default_path]
    search_paths += [bpy.path.abspath(p.path) for p in prefs.additional_import_paths if p.path.strip()]

    for template_dir in search_paths:
        if not os.path.isdir(template_dir):
            print(f"[Blendertools] Skipping missing path: {template_dir}")
            continue

        for file in os.listdir(template_dir):
            if file.lower().endswith(".json"):
                filepath = os.path.join(template_dir, file)
                try:
                    import_template_from_file(filepath)
                    print(f"[Blendertools] Imported template: {filepath}")
                except Exception as e:
                    print(f"[Blendertools] Failed to import {filepath}: {e}")

    return None  # Stop timer
