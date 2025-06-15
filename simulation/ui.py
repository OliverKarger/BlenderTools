import bpy


class VIEW3D_PT_blendertools_simulation(bpy.types.Panel):
    """
    A Blender UI panel for managing simulation tools.

    This class represents a UI panel in Blender's 3D Viewport, providing
    access to various simulation-related tools within the "Blender Tools"
    add-on. It includes options for soft body and collision simulations,
    displayed as part of the add-on's UI in the sidebar.

    Attributes:
        bl_label (str): The label for the panel displayed in the UI. In this case, "Simulation."
        bl_idname (str): The unique identifier for the panel, "VIEW3D_PT_blendertools_simulation."
        bl_space_type (str): The type of space this panel is intended to exist in,
            specified as "VIEW_3D" (the 3D Viewport).
        bl_region_type (str): The type of region in the UI where the panel
            will appear, specified as "UI" (sidebar).
        bl_category (str): The category tab under which this panel will appear,
            specified as "Blender Tools."
    """

    bl_label = "Simulation"
    bl_idname = "VIEW3D_PT_blendertools_simulation"
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
        box.operator("blendertools.sbrebindrecursive")

        box = layout.box()
        box.label(text="Collision")
        box.operator("blendertools.show_collider_overlay")
        box.operator("blendertools.hide_collider_overlay")


def register():
    bpy.utils.register_class(VIEW3D_PT_blendertools_simulation)


def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_blendertools_simulation)
