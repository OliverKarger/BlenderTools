from . import armature
from . import preferences
from . import simulation
from . import cli
from . import camera
from . import utils
from . import lights


bl_info = {
    "name": "Blender Tools",
    "description": "Collection of Blender Utilities",
    "author": "Oliver Karger",
    "version": (2025, 6, 3),
    "blender": (4, 3, 0),
    "doc_url": "https://gitlab.karger.lan/oliver/blendertools",
}


def register():
    utils.register()

    cli.register()
    preferences.register()
    armature.register()
    simulation.register()
    camera.register()
    lights.register()


def unregister():
    cli.unregister()
    simulation.unregister()
    armature.unregister()
    preferences.unregister()
    camera.unregister()
    lights.unregister()

    utils.unregister()


if __name__ == "__main__":
    register()
