from .. import bt_logger
from . import ifo_visualizer
from . import ui

logger = bt_logger.get_logger(__name__)


def register():
    logger.info("Registering Camera Tools")
    ifo_visualizer.register()
    ui.register()


def unregister():
    logger.debug("Unregistering Camera Tools")
    ifo_visualizer.unregister()
    ui.unregister()
