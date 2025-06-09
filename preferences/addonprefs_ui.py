import bpy

from . import addonprefs_props

class BlendertoolsAddonPreferences(bpy.types.AddonPreferences):
    """ Addon Preferences """


    # IMPORTANT: This must match the addon folder name
    bl_idname = "blendertools"

    AutoImportEnabled: bpy.props.BoolProperty(
        name="Enable Auto Import",
        description="Automatically import templates at addon startup",
        default=True
    )

    AdditionalImportPaths: bpy.props.CollectionProperty(
        type=addonprefs_props.TemplatePathItem,
        name="Additional Paths"
    )

    def draw(self, context):
        layout = self.layout

        layout.prop(self, "AutoImportEnabled")

        layout.label(text="Additional Template Paths", icon="FILE_FOLDER")

        box = layout.box()
        for idx, item in enumerate(self.AdditionalImportPaths):
            row = box.row()
            row.prop(item, "path", text=f"Path {idx + 1}")
            op = row.operator("blendertools.remove_template_path", text="", icon="X")
            op.index = idx

        layout.operator("blendertools.add_template_path", icon="ADD")

def register():
    bpy.utils.register_class(BlendertoolsAddonPreferences)

def unregister():
    bpy.utils.unregister_class(BlendertoolsAddonPreferences)