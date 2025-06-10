import bpy

class BlenderTools_RpcRemoteProps(bpy.types.PropertyGroup):
    """ Rpc Remote Server Settings """

    ip: bpy.props.StringProperty(name="IP Address", default="127.0.0.1")
    port: bpy.props.StringProperty(name="Port", default="55643")

    is_active: bpy.props.BoolProperty(name="Is active", default=False)


def register():
    bpy.utils.register_class(BlenderTools_RpcRemoteProps)
    bpy.types.Scene.blendertools_rpcremote = bpy.props.PointerProperty(type=BlenderTools_RpcRemoteProps)

def unregister():
    bpy.utils.unregister_class(BlenderTools_RpcRemoteProps)
    del bpy.types.Scene.blendertools_rpcremote