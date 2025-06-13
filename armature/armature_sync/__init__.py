import logging

from .. import bt_logger

from . import armature_sync_ops
from . import armature_sync_ui
from . import armature_sync_props

logger = bt_logger.get_logger(__name__)

def register():
    logger.info("Registering Armature Sync Tools")
    armature_sync_props.register()
    armature_sync_ops.register()
    armature_sync_ui.register()


def unregister():
    logger.debug("Unregistering Armature Sync Tools")
    armature_sync_ui.unregister()
    armature_sync_ops.unregister()
    armature_sync_props.unregister()
