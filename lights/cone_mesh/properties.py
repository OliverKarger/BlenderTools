import bpy


class BlenderTools_LightConeMeshProps(bpy.types.PropertyGroup):
    light: bpy.props.PointerProperty(
        name="Light", type=bpy.types.Object, poll=lambda self, obj: obj.type == "LIGHT"  # noqa: F821
    )


def register():
    bpy.utils.register_class(BlenderTools_LightConeMeshProps)
    bpy.types.Scene.blendertools_lightconemesh = bpy.props.PointerProperty(type=BlenderTools_LightConeMeshProps)


def unregister():
    bpy.utils.unregister_class(BlenderTools_LightConeMeshProps)
    del bpy.types.Scene.blendertools_lightconemesh
