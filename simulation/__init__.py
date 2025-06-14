from .. import bt_logger

from . import softbody_rebind
from . import collsion_visu

from . import ui

logger = bt_logger.get_logger(__name__)


def register():
    logger.info("Registering Simulation Tools")
    softbody_rebind.register()
    collsion_visu.register()
    ui.register()


def unregister():
    logger.debug("Unregistering Simulation Tools")
    softbody_rebind.unregister()
    collsion_visu.unregister()
    ui.unregister()
