import bpy

from . import addonprefs_props

class BlendertoolsAddonPreferences(bpy.types.AddonPreferences):
    """ Addon Preferences """

    # IMPORTANT: This must match the addon folder name
    bl_idname = "blendertools"

    auto_import_enabled: bpy.props.BoolProperty(
        name="Enable Auto Import",
        description="Automatically import templates at addon startup",
        default=True
    )

    additional_import_paths: bpy.props.CollectionProperty(
        type=addonprefs_props.TemplatePathItem,
        name="Additional Paths"
    )

    enable_armature: bpy.props.BoolProperty(name="Enable Armature Tools", default=True)
    enable_node_groups: bpy.props.BoolProperty(name="Enable Node Group Tools", default=True)
    enable_workflow: bpy.props.BoolProperty(name="Enable Workflows", default=True)
    enable_rpc_remote: bpy.props.BoolProperty(name="Enable RPC Remoting", default=False)

    def draw(self, context):
        layout = self.layout

        # --- Enable Settings Box ---
        enable_box = layout.box()
        enable_box.label(text="Settings", icon="PREFERENCES")
        enable_box.prop(self, "enable_armature")
        enable_box.prop(self, "enable_node_groups")
        enable_box.prop(self, "enable_workflow")
        enable_box.prop(self, "enable_rpc_remote")

        # --- Additional Template Paths (Shown Only if Enabled) ---
        if self.enable_node_groups:
            box = layout.box()
            box.label(text="Node Group Settings")
            box.prop(self, "auto_import_enabled")    
            path_box = box.box()
            path_box.label(text="Additional Import Paths", icon="FILE_FOLDER")
            for idx, item in enumerate(self.additional_import_paths):
                row = path_box.row()
                row.prop(item, "path", text=f"Path {idx + 1}")
                op = row.operator("blendertools.remove_template_path", text="", icon="X")
                op.index = idx

            layout.operator("blendertools.add_template_path", icon="ADD")

def register():
    bpy.utils.register_class(BlendertoolsAddonPreferences)

def unregister():
    bpy.utils.unregister_class(BlendertoolsAddonPreferences)