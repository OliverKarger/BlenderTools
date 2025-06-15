from .. import bt_logger
from . import ngtemplates
from . import ui

logger = bt_logger.get_logger(__name__)


def register():
    logger.info("Registering Node Group Tools")
    ngtemplates.register()
    ui.register()


def unregister():
    logger.debug("Unregistering Node Group Tools")
    ngtemplates.unregister()
    ui.unregister()
