from . import sbrebind_ui
from . import sbrebind_ops

def register():
    sbrebind_ops.register()
    sbrebind_ui.register()

def unregister():
    sbrebind_ui.unregister()
    sbrebind_ops.unregister()