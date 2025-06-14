from . import armature
from . import node_groups
from . import preferences
from . import rpc_remote
from . import simulation
from . import cli

# from . import octane

bl_info = {
    "name": "Blender Tools",
    "description": "Collection of Blender Utilities",
    "author": "Oliver Karger",
    "version": (2025, 0, 0),
    "blender": (4, 3, 0),
    "doc_url": "https://gitlab.karger.lan/oliver/blendertools",
    "warning": "This Addon is still in Development!"
}


def register():
    cli.register()
    preferences.register()
    armature.register()
    node_groups.register()
    rpc_remote.register()
    simulation.register()
    # octane.register()


def unregister():
    cli.unregister()
    simulation.unregister()
    armature.unregister()
    node_groups.unregister()
    preferences.unregister()
    rpc_remote.unregister()
    # octane.unregister()


if __name__ == "__main__":
    register()
