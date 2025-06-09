from . import addonprefs_ops
from . import addonprefs_ui
from . import addonprefs_props

def register():
    addonprefs_props.register()
    addonprefs_ops.register()
    addonprefs_ui.register()

def unregister():
    addonprefs_ui.unregister()
    addonprefs_ops.unregister()
    addonprefs_props.unregister()