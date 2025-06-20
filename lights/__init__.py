from .. import bt_logger
from . import cone_mesh
from . import ui

logger = bt_logger.get_logger(__name__)


def register():
    logger.info("Registering Light Tools")
    cone_mesh.register()
    ui.register()


def unregister():
    logger.debug("Unregistering Light Tools")
    cone_mesh.unregister()
    ui.unregister()
