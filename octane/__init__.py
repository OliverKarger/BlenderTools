from . import light_converter

from .. import bt_logger
logger = bt_logger.get_logger(__name__)

def register():
    logger.info("Registering Octane Tools")
    # light_converter.register()

def unregister():
    logger.debug("Unregistering Octane Tools")
    # light_converter.unregister()