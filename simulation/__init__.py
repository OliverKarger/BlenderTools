from .. import bt_logger

from . import softbody_rebind
from . import collision_visualizer
from . import proxy_generator

from . import ui

logger = bt_logger.get_logger(__name__)


def register():
    logger.info("Registering Simulation Tools")
    softbody_rebind.register()
    collision_visualizer.register()
    proxy_generator.register()
    ui.register()


def unregister():
    logger.debug("Unregistering Simulation Tools")
    softbody_rebind.unregister()
    collision_visualizer.unregister()
    proxy_generator.unregister()
    ui.unregister()
