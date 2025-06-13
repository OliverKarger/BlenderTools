import logging

from .. import bt_logger

from . import operators
from . import ui
from . import properties

logger = bt_logger.get_logger(__name__)


def register():
    logger.info("Registering Armature Sync Tools")
    properties.register()
    operators.register()
    ui.register()


def unregister():
    logger.debug("Unregistering Armature Sync Tools")
    ui.unregister()
    operators.unregister()
    properties.unregister()
