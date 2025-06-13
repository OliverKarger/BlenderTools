from .. import bt_logger

from . import ui
from . import properties
from . import operators

logger = bt_logger.get_logger(__name__)

def register():
    logger.info("Registering RPC Remote Tools")
    properties.register()
    ui.register()
    operators.register()


def unregister():
    logger.debug("Unregistering RPC Remote Tools")
    operators.unregister()
    ui.unregister()
    properties.unregister()
