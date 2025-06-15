from . import bt_logger

logger = bt_logger.get_logger(__name__)


def register():
    logger.info("Registering CLI")


def unregister():
    logger.debug("Unregistering CLI")
