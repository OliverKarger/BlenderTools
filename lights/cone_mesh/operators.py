import bpy

from .. import utils


class BlenderTools_LightVolume_Create(bpy.types.Operator):
    bl_idname = "blendertools.lightvolume_create"
    bl_label = "Create Light Volume"

    add_volumetric_shader: bpy.props.BoolProperty(name="Add Default Volumetric Shader", default=False)
    set_parent: bpy.props.BoolProperty(name="Set Light Source as Parent", default=True)
    scale_factor: bpy.props.FloatProperty(name="Scale Factor", default=1)
    distance: bpy.props.FloatProperty(name="Distance", default=10.0)  # noqa: F821

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "add_volumetric_shader")
        layout.prop(self, "set_parent")
        layout.prop(self, "scale_factor")
        layout.prop(self, "distance")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        props = context.scene.blendertools_lightconemesh
        addon = context.preferences.addons.get("blendertools")

        if addon.preferences.settings.viewport_selector_enabled:
            if not context.active_object:
                self.report({"ERROR"}, "Please select a Object")
                return {"CANCELLED"}
            if not context.active_object.type == "LIGHT":
                self.report({"ERROR"}, "Please select a Light!")
                return {"CANCELLED"}

            light_data = context.active_object.data
        else:
            light_data = props.light.data

        light_type = light_data.type

        if light_type == "SPOT":
            mesh_obj = utils.mesh.create_spot_volume_cone(
                props.light, self.scale_factor, 64, self.distance, self.set_parent
            )
        elif light_type == "AREA":
            mesh_obj = utils.mesh.create_area_volume_box(props.light, self.scale_factor, self.set_parent, self.distance)
        else:
            self.report({"WARNING"}, f"Light Type {light_type} not supported!")
            return {"CANCELLED"}

        if self.set_parent:
            mesh_obj.location = props.light.location
            mesh_obj.parent = props.light
            mesh_obj.matrix_parent_inverse = props.light.matrix_world.inverted()

        if self.add_volumetric_shader:
            utils.shader.add_volumetric_material(mesh_obj)

        return {"FINISHED"}


def register():
    bpy.utils.register_class(BlenderTools_LightVolume_Create)


def unregister():
    bpy.utils.unregister_class(BlenderTools_LightVolume_Create)
