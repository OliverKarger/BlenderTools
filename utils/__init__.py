from . import icons  # noqa: F401
from . import viewport_visualizer  # noqa: F401
from . import color  # noqa: F401


def register():
    icons.IconManager.register()


def unregister():
    icons.IconManager.unregister()
