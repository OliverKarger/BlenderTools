from . import rpc_remote_ui
from . import rpc_remote_props
from . import rpc_remote_ops


def register():
    rpc_remote_props.register()
    rpc_remote_ui.register()
    rpc_remote_ops.register()


def unregister():
    rpc_remote_ops.unregister()
    rpc_remote_ui.unregister()
    rpc_remote_props.unregister()
