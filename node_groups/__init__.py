import bpy

from . import ngtemplates_ops
from . import ngtemplates_ui
from . import ngtemplates_utils

def register():
    ngtemplates_ops.register()
    ngtemplates_ui.register()

    # Needs to run later so the Python Environment is fully initialized/available
    bpy.app.timers.register(ngtemplates_utils.auto_import_templates, first_interval=1)

def unregister():
    ngtemplates_ops.unregister()
    ngtemplates_ui.unregister()