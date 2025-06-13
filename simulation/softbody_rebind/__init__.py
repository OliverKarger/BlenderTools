from .. import bt_logger

from . import ui
from . import operators

logger = bt_logger.get_logger(__name__)


def register():
    logger.info("Registering Softbody Rebind Tools")
    operators.register()
    ui.register()


def unregister():
    logger.debug("Unregistering Softbody Rebind Tools")
    ui.unregister()
    operators.unregister()
