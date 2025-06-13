from .. import bt_logger

from . import sbrebind_ui
from . import sbrebind_ops

logger = bt_logger.get_logger(__name__)

def register():
    logger.info("Registering Softbody Rebind Tools")
    sbrebind_ops.register()
    sbrebind_ui.register()


def unregister():
    logger.info("Unregistering Softbody Rebind Tools")
    sbrebind_ui.unregister()
    sbrebind_ops.unregister()
