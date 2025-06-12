from . import addonprefs_ops
from . import addonprefs_ui
from . import addonprefs_props


def register():
    addonprefs_props.register()
    addonprefs_ui.register()
    addonprefs_ops.register()


def unregister():
    addonprefs_ops.unregister()
    addonprefs_ui.unregister()
    addonprefs_props.unregister()
