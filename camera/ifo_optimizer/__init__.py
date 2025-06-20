from . import operators
from . import properties


def register():
    operators.register()
    properties.register()


def unregister():
    operators.unregister()
    properties.unregister()
