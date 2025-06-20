import bpy

from . import utils


class __BlenderTools_ProxyGeneratorBase__(bpy.types.Operator):
    decimate_factor: bpy.props.FloatProperty(name="Decimate Factor", default=1.0, min=0.0, max=1.0)
    parent: bpy.props.BoolProperty(name="Parent", default=True)  # noqa: F821
    hide_render: bpy.props.BoolProperty(name="Hide in Render", default=True)  # noqa: F821
    hide_viewport: bpy.props.BoolProperty(name="Hide in Viewport", default=False)  # noqa: F821

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "decimate_factor")
        layout.prop(self, "parent")
        layout.prop(self, "hide_render")
        layout.prop(self, "hide_viewport")


class BlenderTools_CollisionProxyGenerator(__BlenderTools_ProxyGeneratorBase__):
    bl_idname = "blendertools.collision_proxy_generator"
    bl_label = "Generate Collision Proxy"

    def execute(self, context):
        obj, proxy = utils.generate_proxy(context, self, "COLLISION")
        return {"FINISHED"} if proxy else {"CANCELLED"}


class BlenderTools_SoftbodyProxyGenerator(__BlenderTools_ProxyGeneratorBase__):
    bl_idname = "blendertools.softbody_proxy_generator"
    bl_label = "Generate Softbody Proxy"

    def execute(self, context):
        obj, proxy = utils.generate_proxy(context, self, "SOFT_BODY")
        return {"FINISHED"} if proxy else {"CANCELLED"}


class BlenderTools_ClothProxyGenerator(__BlenderTools_ProxyGeneratorBase__):
    bl_idname = "blendertools.cloth_proxy_generator"
    bl_label = "Generate Cloth Proxy"

    def execute(self, context):
        obj, proxy = utils.generate_proxy(context, self, "CLOTH")
        return {"FINISHED"} if proxy else {"CANCELLED"}


def register():
    bpy.utils.register_class(BlenderTools_ClothProxyGenerator)
    bpy.utils.register_class(BlenderTools_SoftbodyProxyGenerator)
    bpy.utils.register_class(BlenderTools_CollisionProxyGenerator)


def unregister():
    bpy.utils.unregister_class(BlenderTools_ClothProxyGenerator)
    bpy.utils.unregister_class(BlenderTools_SoftbodyProxyGenerator)
    bpy.utils.unregister_class(BlenderTools_CollisionProxyGenerator)
