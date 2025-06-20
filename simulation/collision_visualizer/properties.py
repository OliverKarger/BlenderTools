import bpy


class BlenderTools_CollisionVisualizer_ColliderNameEntry(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()


class BlenderTools_CollisionVisualizerProps(bpy.types.PropertyGroup):
    overlay_handle = bpy.props.IntProperty(default=-1)
    collider_names: bpy.props.CollectionProperty(type=BlenderTools_CollisionVisualizer_ColliderNameEntry)


def register():
    bpy.utils.register_class(BlenderTools_CollisionVisualizer_ColliderNameEntry)
    bpy.utils.register_class(BlenderTools_CollisionVisualizerProps)
    bpy.types.Scene.blendertools_collisionvisu = bpy.props.PointerProperty(type=BlenderTools_CollisionVisualizerProps)


def unregister():
    bpy.utils.unregister_class(BlenderTools_CollisionVisualizerProps)
    bpy.utils.unregister_class(BlenderTools_CollisionVisualizer_ColliderNameEntry)
    del bpy.types.Scene.blendertools_collisionvisu
