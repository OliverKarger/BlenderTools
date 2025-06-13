from .. import bt_logger

from . import rpc_remote_ui
from . import rpc_remote_props
from . import rpc_remote_ops

logger = bt_logger.get_logger(__name__)

def register():
    logger.info("Registering RPC Remote Tools")
    rpc_remote_props.register()
    rpc_remote_ui.register()
    rpc_remote_ops.register()


def unregister():
    logger.debug("Unregistering RPC Remote Tools")
    rpc_remote_ops.unregister()
    rpc_remote_ui.unregister()
    rpc_remote_props.unregister()
