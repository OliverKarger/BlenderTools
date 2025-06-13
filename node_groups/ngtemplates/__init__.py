import bpy

from .. import bt_logger
from . import operators
from . import ui

logger = bt_logger.get_logger(__name__)

def register():
    logger.info("Registering Node Group Tools")
    operators.register()
    ui.register()

    # Needs to run later so the Python Environment is fully initialized/available
    # bpy.app.timers.register(ngtemplates_utils.auto_import_templates, first_interval=5)


def unregister():
    logger.debug("Unregistering Node Group Tools")
    operators.unregister()
    ui.unregister()
