from . import armature_sync_ops
from . import armature_sync_ui
from . import armature_sync_props


def register():
    armature_sync_props.register()
    armature_sync_ops.register()
    armature_sync_ui.register()


def unregister():
    armature_sync_ui.unregister()
    armature_sync_ops.unregister()
    armature_sync_props.unregister()
