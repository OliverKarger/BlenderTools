from . import armature
from . import node_groups
from . import preferences
from . import simulation
from . import cli
from . import camera
from . import utils

bl_info = {
    "name": "Blender Tools",
    "description": "Collection of Blender Utilities",
    "author": "Oliver Karger",
    "version": (2025, 6, 2),
    "blender": (4, 3, 0),
    "doc_url": "https://gitlab.karger.lan/oliver/blendertools",
}


def register():
    utils.register()

    cli.register()
    preferences.register()
    armature.register()
    node_groups.register()
    simulation.register()
    camera.register()


def unregister():
    cli.unregister()
    simulation.unregister()
    armature.unregister()
    node_groups.unregister()
    preferences.unregister()
    camera.unregister()

    utils.unregister()


if __name__ == "__main__":
    register()
