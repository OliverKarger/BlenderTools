import bpy


class BlenderTools_IfoOptimizer_Item(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Object Name")

    hidden_viewport: bpy.props.BoolProperty("Was hidden in Viewport")
    disabled_viewport: bpy.props.BoolProperty("Was disabled in Viewport")
    hidden_render: bpy.props.BoolProperty("Was hidden in Render")

    object_type: bpy.props.StringProperty("Object Type")


class BlenderTools_IfoOptimizerProps(bpy.types.PropertyGroup):
    hidden_objects: bpy.props.CollectionProperty(name="Hidden Objects", type=BlenderTools_IfoOptimizer_Item)
    active_item_index: bpy.props.IntProperty("Active Item Index")
    camera: bpy.props.PointerProperty(
        name="Camera", type=bpy.types.Object, poll=lambda self, obj: obj.type == "CAMERA"  # noqa:F821
    )


def register():
    bpy.utils.register_class(BlenderTools_IfoOptimizer_Item)
    bpy.utils.register_class(BlenderTools_IfoOptimizerProps)
    bpy.types.Scene.blendertools_ifooptimizer = bpy.props.PointerProperty(type=BlenderTools_IfoOptimizerProps)


def unregister():
    bpy.utils.unregister_class(BlenderTools_IfoOptimizerProps)
    bpy.utils.unregister_class(BlenderTools_IfoOptimizer_Item)
    del bpy.types.Scene.blendertools_ifooptimizer
