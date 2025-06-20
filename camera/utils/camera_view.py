import mathutils
import bmesh
from mathutils.geometry import normal
from mathutils.bvhtree import BVHTree
from bpy_extras.object_utils import world_to_camera_view
from ... import bt_logger

logger = bt_logger.get_logger(__name__)


def get_camera_view_planes(scene, camera_obj):
    camera = camera_obj.data
    matrix = camera_obj.matrix_world.normalized()
    frame = [matrix @ v for v in camera.view_frame(scene=scene)]
    origin = matrix.to_translation()

    planes = []
    is_perspective = camera.type != "ORTHO"

    for i in range(4):
        third = origin if is_perspective else frame[i] + matrix.col[2].xyz
        n = normal(third, frame[i - 1], frame[i])
        d = -n.dot(third)
        planes.append((n, d))

    if not is_perspective:
        n = normal(frame[0], frame[1], frame[2])
        d = -n.dot(origin)
        planes.append((n, d))

    logger.info(f"Found {len(planes)} View Plates of Camera {camera_obj.name}")
    return planes


def is_bounding_box_in_frustum(obj_eval, planes, margin=0.01):
    """
    Returns True if any point of the object's bounding box is inside all planes.
    Allows a small margin to catch near misses.
    """
    corners = [obj_eval.matrix_world @ mathutils.Vector(corner) for corner in obj_eval.bound_box]

    for corner in corners:
        inside = True
        for normal, d in planes:  # noqa: F402
            if normal.dot(corner) + d < -margin:
                inside = False
                break
        if inside:
            return True

    return False


def is_origin_in_camera_view(scene, camera, obj_eval):
    origin_world = obj_eval.matrix_world.translation
    co_ndc = world_to_camera_view(scene, camera, origin_world)
    return (
        0.0 <= co_ndc.x <= 1.0 and 0.0 <= co_ndc.y <= 1.0 and camera.data.clip_start <= co_ndc.z <= camera.data.clip_end
    )


def is_camera_inside_object(obj_eval, camera_location):
    """
    Returns True if the camera is inside the object's mesh using ray casting.
    Uses BVHTree.FromBMesh to handle cases where FromMesh is unavailable.
    """
    if obj_eval.type != "MESH":
        return False

    mesh = obj_eval.to_mesh()
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bm.transform(obj_eval.matrix_world)

    bvh = BVHTree.FromBMesh(bm)
    bm.free()
    obj_eval.to_mesh_clear()

    directions = [
        mathutils.Vector((1, 0, 0)),
        mathutils.Vector((0, 1, 0)),
        mathutils.Vector((0, 0, 1)),
        mathutils.Vector((-1, 0, 0)),
        mathutils.Vector((0, -1, 0)),
        mathutils.Vector((0, 0, -1)),
    ]

    hits = 0
    for dir in directions:
        loc, norm, index, dist = bvh.ray_cast(camera_location, dir, 1e6)
        if loc is not None:
            hits += 1

    return hits % 2 == 1


def is_mesh_partially_visible(context, camera, obj_eval, sample_limit=100):
    """
    Sample the object's mesh vertices and check if any are visible in camera view.
    Useful for catching partial visibility cases.
    """
    if obj_eval.type != "MESH":
        return False

    scene = context.scene
    cam = camera
    mesh = obj_eval.to_mesh()
    mesh.transform(obj_eval.matrix_world)

    vertices = mesh.vertices
    total = len(vertices)
    step = max(1, total // sample_limit)

    for i in range(0, total, step):
        v = vertices[i].co
        co_ndc = world_to_camera_view(scene, cam, v)
        if 0.0 <= co_ndc.x <= 1.0 and 0.0 <= co_ndc.y <= 1.0 and cam.data.clip_start <= co_ndc.z <= cam.data.clip_end:
            obj_eval.to_mesh_clear()
            return True

    obj_eval.to_mesh_clear()
    return False


def get_objects_in_camera_view(context, camera):
    scene = context.scene
    depsgraph = context.evaluated_depsgraph_get()
    cam_loc = camera.matrix_world.translation
    planes = get_camera_view_planes(scene, camera)

    visible_objects = []

    for obj in scene.objects:
        if obj.type != "MESH" or not obj.visible_get():
            continue

        obj_eval = obj.evaluated_get(depsgraph)

        if (
            is_bounding_box_in_frustum(obj_eval, planes, margin=0.05)
            or is_origin_in_camera_view(scene, camera, obj_eval)  # noqa: W503
            or is_camera_inside_object(obj_eval, cam_loc)  # noqa: W503
            or is_mesh_partially_visible(context, camera, obj_eval, sample_limit=100)  # noqa: W503
        ):
            visible_objects.append(obj)

    return visible_objects
