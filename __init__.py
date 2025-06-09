bl_info = {
    "name": "Blender Tools",
    "description": "Collection of Blender Utilities",
    "author": "Oliver Karger",
    "version": (2025, 0, 0),
    "blender": (4, 3, 0),
    "doc_url": "https://gitlab.karger.lan/oliver/blendertools",
}

from . import armature
from . import node_groups
from . import preferences

def register():
    preferences.register()
    armature.register()
    node_groups.register()

def unregister():
    armature.unregister()
    node_groups.unregister()
    preferences.unregister()

if __name__ == "__main__":
    register()