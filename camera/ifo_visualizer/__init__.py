from . import properties
from . import operators


def register():
    properties.register()
    operators.register()


def unregister():
    operators.unregister()
    properties.unregister()
