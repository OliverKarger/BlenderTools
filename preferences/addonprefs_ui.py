import bpy

from . import addonprefs_props

class BlendertoolsAddonPreferences(bpy.types.AddonPreferences):
    # IMPORTANT: This must match the addon folder name
    bl_idname = "blendertools"

    auto_import_enabled: bpy.props.BoolProperty(
        name="Enable Auto Import",
        description="Automatically import templates at addon startup",
        default=True
    )

    additional_paths: bpy.props.CollectionProperty(
        type=addonprefs_props.TemplatePathItem,
        name="Additional Paths"
    )

    def draw(self, context):
        layout = self.layout

        layout.prop(self, "auto_import_enabled")

        layout.label(text="Additional Template Paths", icon="FILE_FOLDER")

        box = layout.box()
        for idx, item in enumerate(self.additional_paths):
            row = box.row()
            row.prop(item, "path", text=f"Path {idx + 1}")
            op = row.operator("blendertools.remove_template_path", text="", icon="X")
            op.index = idx

        layout.operator("blendertools.add_template_path", icon="ADD")

def register():
    bpy.utils.register_class(BlendertoolsAddonPreferences)

def unregister():
    bpy.utils.unregister_class(BlendertoolsAddonPreferences)