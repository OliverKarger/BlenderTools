from .. import bt_logger
from . import armature_sync

logger = bt_logger.get_logger(__name__)

def register():
    logger.info("Registering Armature Tools")
    armature_sync.register()

def unregister():
    logger.debug("Unregistering Armature Tools")
    armature_sync.unregister()