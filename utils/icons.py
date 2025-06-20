import os

from bpy.utils import previews

ICON_MAP = {
    "MESH": "MESH_DATA",
    "LIGHT": "LIGHT_DATA",
    "LIGHT_PROBE": "LIGHT_DATA",
    "CAMERA": "CAMERA_DATA",
    "CURVE": "CURVE_DATA",
    "EMPTY": "EMPTY_DATA",
    "ARMATURE": "ARMATURE_DATA",
    "LATTICE": "LATTICE_DATA",
    "META": "META_DATA",
    "FONT": "FONT_DATA",
    "SPEAKER": "SPEAKER",
    "VOLUME": "VOLUME_DATA",
}


class IconManager:
    """
    Manages and registers custom icons for use within the Blender interface.

    The IconManager class provides a mechanism to manage custom icons through Blender's
    preview image collections. It handles loading, registering, and unregistering icons,
    as well as retrieving their unique icon IDs for Blender UI elements. This class is
    designed to work specifically within the Blender scripting environment.
    """

    _preview_collections = {}
    _icon_name = "blendertools_icon"
    _collection_key = "main"
    _icon_filename = "blendertools.png"

    @classmethod
    def register(cls):
        if cls._collection_key in cls._preview_collections:
            return  # Already registered

        pcoll = previews.new()

        icon_path = os.path.join(os.path.dirname(__file__), "..", cls._icon_filename)
        if not os.path.exists(icon_path):
            print(f"[IconManager] Warning: Icon file not found: {icon_path}")
        else:
            pcoll.load(cls._icon_name, icon_path, "IMAGE")

        cls._preview_collections[cls._collection_key] = pcoll

    @classmethod
    def unregister(cls):
        for pcoll in cls._preview_collections.values():
            previews.remove(pcoll)
        cls._preview_collections.clear()

    @classmethod
    def get_icon_id(cls, name=None):
        """Returns the icon ID, optionally by custom name."""
        key = name or cls._icon_name
        pcoll = cls._preview_collections.get(cls._collection_key)
        if pcoll and key in pcoll:
            return pcoll[key].icon_id
        return 0  # default icon_id fallback
