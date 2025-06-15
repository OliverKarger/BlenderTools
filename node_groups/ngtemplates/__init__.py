from .. import bt_logger
from . import operators

logger = bt_logger.get_logger(__name__)


def register():
    logger.info("Registering Node Group Tools")
    operators.register()


def unregister():
    logger.debug("Unregistering Node Group Tools")
    operators.unregister()
