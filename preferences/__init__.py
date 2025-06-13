from .. import bt_logger

from . import operators
from . import ui
from . import properties

logger = bt_logger.get_logger(__name__)

def register():
    logger.info("Registering Preferences")
    properties.register()
    ui.register()
    operators.register()


def unregister():
    logger.debug("Unregistering Preferences")
    operators.unregister()
    ui.unregister()
    properties.unregister()
