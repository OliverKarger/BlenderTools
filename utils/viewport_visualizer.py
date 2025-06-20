import gpu
from gpu_extras.batch import batch_for_shader
from .. import bt_logger

logger = bt_logger.get_logger(__name__)


def build_wireframe_batches(objects, cache):
    """
    Build GPU wireframe batches for the given objects and store in the provided cache.

    Args:
        objects (list of bpy.types.Object): Mesh objects to draw.
        cache (dict): Dictionary to store the generated batches.
    """
    cache.clear()
    shader = gpu.shader.from_builtin("UNIFORM_COLOR")

    for obj in objects:
        if obj.type != "MESH" or not obj.visible_get():
            continue

        try:
            mesh = obj.to_mesh()
            if not mesh:
                continue

            verts = [obj.matrix_world @ v.co for v in mesh.vertices]
            edges = [(e.vertices[0], e.vertices[1]) for e in mesh.edges]
            batch = batch_for_shader(shader, "LINES", {"pos": verts}, indices=edges)

            cache[obj.name] = batch
            obj.to_mesh_clear()
            logger.info(f"Computed Wireframe Cache for {len(cache)} Objects")

        except Exception as e:
            logger.error(f"Error creating batch for {obj.name}: {e}")


def draw_objects_wireframe(context, objects, cache, color=(1.0, 0.0, 0.0, 1.0)):
    """
    Draw wireframes using prebuilt batches from the given cache.

    Args:
        context: Blender context.
        objects: List of objects to draw.
        cache: Dict of object name → batch.
        color: RGBA tuple for wireframe color.
    """
    shader = gpu.shader.from_builtin("UNIFORM_COLOR")
    shader.bind()
    shader.uniform_float("color", color)

    for obj in objects:
        if not obj.visible_get():
            continue
        batch = cache.get(obj.name)
        if batch:
            batch.draw(shader)
