from .. import bt_logger
from . import ngtemplates

logger = bt_logger.get_logger(__name__)

def register():
    logger.info("Registering Node Group Tools")
    ngtemplates.register()

def unregister():
    logger.info("Unregistering Node Group Tools")
    ngtemplates.unregister()