import bpy

from . import softbody_rebind
from . import collision_visualizer
from . import proxy_generator


class BlenderTools_SimulationPanel(bpy.types.Panel):
    bl_label = "Simulation"
    bl_idname = "BlenderTools_SimulationPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Blender Tools"

    @classmethod
    def poll(cls, context):
        addon = context.preferences.addons.get("blendertools")
        return addon and addon.preferences.simulation.enabled

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        box.label(text="Softbody")
        box.operator(softbody_rebind.operators.BlenderTools_SoftbodyRebind_Rebind.bl_idname, icon="MOD_SOFT")

        box = layout.box()
        box.label(text="Collision")
        box.operator(
            collision_visualizer.operators.BlenderTools_CollisionVisualizer_ShowOverlay.bl_idname, icon="HIDE_OFF"
        )
        box.operator(
            collision_visualizer.operators.BlenderTools_CollisionVisualizer_HideOverlay.bl_idname, icon="HIDE_ON"
        )

        box = layout.box()
        box.label(text="Proxy Generator")
        box.operator(proxy_generator.operators.BlenderTools_ClothProxyGenerator.bl_idname, icon="MOD_CLOTH")
        box.operator(proxy_generator.operators.BlenderTools_SoftbodyProxyGenerator.bl_idname, icon="MOD_SOFT")
        box.operator(proxy_generator.operators.BlenderTools_CollisionProxyGenerator.bl_idname, icon="MOD_PHYSICS")


def register():
    bpy.utils.register_class(BlenderTools_SimulationPanel)


def unregister():
    bpy.utils.unregister_class(BlenderTools_SimulationPanel)
