import bpy

from ... import bt_logger

logger = bt_logger.get_logger(__name__)


def add_volumetric_material(obj: bpy.types.Object):

    # Create new material
    mat = bpy.data.materials.new(name="VolumeMaterial")
    mat.use_nodes = True
    if bpy.context.scene.render.engine == "BLENDER_EEVEE":
        mat.blend_method = "BLEND"
        mat.shadow_method = "HASHED"
    mat.use_screen_refraction = True

    # Clear default nodes
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Create nodes
    output = nodes.new(type="ShaderNodeOutputMaterial")
    output.location = (800, 0)

    mix_shader = nodes.new(type="ShaderNodeMixShader")
    mix_shader.location = (600, 0)
    mix_shader.inputs["Fac"].default_value = 0.5

    principled_volume = nodes.new(type="ShaderNodeVolumePrincipled")
    principled_volume.location = (300, 100)
    principled_volume.inputs["Density"].default_value = 0.25
    principled_volume.inputs["Anisotropy"].default_value = 0.5

    volume_scatter = nodes.new(type="ShaderNodeVolumeScatter")
    volume_scatter.location = (300, -100)
    volume_scatter.inputs["Density"].default_value = 0.25
    volume_scatter.inputs["Anisotropy"].default_value = 0.5

    val_node1 = nodes.new(type="ShaderNodeValue")
    val_node1.name = "Density"
    val_node1.location = (0, 150)
    val_node1.outputs[0].default_value = 0.5

    val_node2 = nodes.new(type="ShaderNodeValue")
    val_node2.name = "Anisotropy"
    val_node2.location = (0, 50)
    val_node2.outputs[0].default_value = 0.25

    rgb_node = nodes.new(type="ShaderNodeRGB")
    rgb_node.name = "Color"
    rgb_node.location = (0, -100)
    rgb_node.outputs[0].default_value = [1.0, 1.0, 1.0, 1.0]

    # Link nodes
    links.new(principled_volume.outputs["Volume"], mix_shader.inputs[1])
    links.new(volume_scatter.outputs["Volume"], mix_shader.inputs[2])
    links.new(mix_shader.outputs["Shader"], output.inputs["Volume"])

    # Connect values and RGB
    links.new(val_node1.outputs[0], principled_volume.inputs["Anisotropy"])
    links.new(val_node2.outputs[0], principled_volume.inputs["Density"])
    links.new(rgb_node.outputs[0], principled_volume.inputs["Color"])

    links.new(val_node1.outputs[0], volume_scatter.inputs["Anisotropy"])
    links.new(val_node2.outputs[0], volume_scatter.inputs["Density"])
    links.new(rgb_node.outputs[0], volume_scatter.inputs["Color"])

    # Assign material to object
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)
