from .. import bt_logger

from ..armature import preferences as armature_preferences
from ..camera import preferences as camera_preferences
from ..cli import preferences as cli_preferences
from ..simulation import preferences as simulation_preferences
from ..lights import preferences as lights_preferences
from . import settings

from . import ui

logger = bt_logger.get_logger(__name__)


def register():
    logger.info("Registering Preferences")
    settings.register()
    armature_preferences.register()
    camera_preferences.register()
    cli_preferences.register()
    simulation_preferences.register()
    lights_preferences.register()
    ui.register()


def unregister():
    logger.debug("Unregistering Preferences")
    armature_preferences.unregister()
    camera_preferences.unregister()
    cli_preferences.unregister()
    simulation_preferences.unregister()
    lights_preferences.unregister()
    ui.unregister()
    settings.unregister()
