import bpy


class BlenderTools_IfoVisualizer_ColliderNameEntry(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()


class BlenderTools_IfoVisualizerProps(bpy.types.PropertyGroup):
    camera: bpy.props.PointerProperty(
        name="Camera", type=bpy.types.Object, poll=lambda self, obj: obj.type == "CAMERA"  # noqa:F821
    )

    overlay_handle = bpy.props.IntProperty(default=-1)

    collider_names: bpy.props.CollectionProperty(type=BlenderTools_IfoVisualizer_ColliderNameEntry)


def register():
    bpy.utils.register_class(BlenderTools_IfoVisualizer_ColliderNameEntry)
    bpy.utils.register_class(BlenderTools_IfoVisualizerProps)
    bpy.types.Scene.blendertools_ifovisualizer = bpy.props.PointerProperty(type=BlenderTools_IfoVisualizerProps)


def unregister():
    bpy.utils.unregister_class(BlenderTools_IfoVisualizerProps)
    bpy.utils.unregister_class(BlenderTools_IfoVisualizer_ColliderNameEntry)
    del bpy.types.Scene.blendertools_ifovisualizer
