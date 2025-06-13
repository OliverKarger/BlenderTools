from .. import bt_logger

from . import addonprefs_ops
from . import addonprefs_ui
from . import addonprefs_props

logger = bt_logger.get_logger(__name__)

def register():
    logger.info("Registering Preferences")
    addonprefs_props.register()
    addonprefs_ui.register()
    addonprefs_ops.register()


def unregister():
    logger.debug("Unregistering Preferences")
    addonprefs_ops.unregister()
    addonprefs_ui.unregister()
    addonprefs_props.unregister()
