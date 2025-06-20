import bpy
import math
from mathutils import Vector


def create_spot_volume_cone(light_obj: bpy.types.Object, scale_factor, segments=64, distance=10.0, use_parent=False):
    light_data = light_obj.data
    angle = light_data.spot_size
    distance = light_data.cutoff_distance if light_data.use_custom_distance else distance
    radius = math.tan(angle / 2) * distance

    # Create cone aligned along +Z at origin
    bpy.ops.mesh.primitive_cone_add(
        vertices=segments,
        radius1=radius * scale_factor,
        radius2=0.0,  # tip
        depth=distance,
        enter_editmode=False,
        location=(0, 0, 0),
        rotation=(0, 0, 0),
    )

    obj = bpy.context.active_object
    obj.name = f"{light_obj.name}_VolumeCone"

    # Enter edit mode to shift geometry so origin is at tip
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.transform.translate(value=(0, 0, -distance / 2))
    bpy.ops.object.mode_set(mode="OBJECT")

    # Set object location to match light
    obj.location = light_obj.location.copy()

    # Set object rotation to exactly match light
    obj.rotation_euler = light_obj.rotation_euler.copy()

    # Parent if needed
    if use_parent:
        obj.parent = light_obj

    return obj


def create_area_volume_box(light_obj, scale_factor, use_parent, distance=10.0):
    light_data = light_obj.data
    base_width = light_data.size
    base_height = light_data.size_y if light_data.shape == "RECTANGLE" else base_width

    # === Bottom face (base of light, unscaled) ===
    w = base_width / 2
    h = base_height / 2
    v0 = Vector((-w, -h, 0))
    v1 = Vector((w, -h, 0))
    v2 = Vector((w, h, 0))
    v3 = Vector((-w, h, 0))

    # === Top face (scaled at "distance" along local -Z) ===
    sw = base_width * scale_factor / 2
    sh = base_height * scale_factor / 2
    v4 = Vector((-sw, -sh, distance))
    v5 = Vector((sw, -sh, distance))
    v6 = Vector((sw, sh, distance))
    v7 = Vector((-sw, sh, distance))

    verts = [v0, v1, v2, v3, v4, v5, v6, v7]
    faces = [(0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]  # bottom  # top

    mesh_data = bpy.data.meshes.new(f"{light_obj.name}_VolumeBox")
    mesh_data.from_pydata(verts, [], faces)
    mesh_data.update()

    obj = bpy.data.objects.new(f"{light_obj.name}_VolumeBoxObj", mesh_data)
    bpy.context.collection.objects.link(obj)

    # Rotate to match -Z emission of the Area light
    obj.rotation_euler = (math.radians(180), 0, 0)

    if use_parent:
        obj.parent = light_obj

    return obj
