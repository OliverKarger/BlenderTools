from . import operators
from . import properties


def register():
    properties.register()
    operators.register()


def unregister():
    operators.unregister()
    properties.unregister()
