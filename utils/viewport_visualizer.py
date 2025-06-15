import gpu
from gpu_extras.batch import batch_for_shader


def draw_objects_wireframe(context, objects, color=(1.0, 0.0, 0.0, 1.0)):
    """
    Draw objects in a wireframe style using a specified color.

    The function renders a list of given 3D objects as wireframes in the Blender viewport.
    The wireframe rendering is done using the provided color and the object's vertices and
    edges information. Non-visible objects and objects without associated mesh data are
    ignored during the drawing process.

    Parameters:
        context (bpy.types.Context): Context of the current Blender operation.
        objects (List[bpy.types.Object]): List of Blender objects to be rendered in wireframe.
        color (Tuple[float, float, float, float], optional): RGBA color for the wireframe.
            Default is (1.0, 0.0, 0.0, 1.0).

    Raises:
        None

    Returns:
        None
    """
    shader = gpu.shader.from_builtin("UNIFORM_COLOR")
    shader.bind()
    shader.uniform_float("color", color)

    for obj in objects:
        if not obj.visible_get():
            continue

        mesh = obj.to_mesh()
        if not mesh:
            continue

        verts = [obj.matrix_world @ v.co for v in mesh.vertices]
        edges = [(e.vertices[0], e.vertices[1]) for e in mesh.edges]

        batch = batch_for_shader(shader, "LINES", {"pos": verts}, indices=edges)
        batch.draw(shader)
        obj.to_mesh_clear()
