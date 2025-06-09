from . import ngtemplates_ops
from . import ngtemplates_ui

def register():
    ngtemplates_ops.register()
    ngtemplates_ui.register()

def unregister():
    ngtemplates_ops.unregister()
    ngtemplates_ui.unregister()