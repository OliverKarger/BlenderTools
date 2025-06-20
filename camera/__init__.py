from .. import bt_logger
from . import ifo_visualizer
from . import ui
from . import ifo_optimizer

logger = bt_logger.get_logger(__name__)


def register():
    logger.info("Registering Camera Tools")
    ifo_visualizer.register()
    ifo_optimizer.register()
    ui.register()


def unregister():
    logger.debug("Unregistering Camera Tools")
    ui.unregister()
    ifo_optimizer.unregister()
    ifo_visualizer.unregister()
