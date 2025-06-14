from .. import bt_logger

from . import operators
from . import ui

logger = bt_logger.get_logger(__name__)


def register():
    logger.info("Registering Collision Visualization Tools")
    operators.register()
    ui.register()


def unregister():
    logger.debug("Unregistering Collision Visualization Tools")
    operators.unregister()
    ui.unregister()
