import bpy

from . import addonprefs_props


class BlendertoolsAddonPreferences(bpy.types.AddonPreferences):
    """Addon Preferences"""

    # IMPORTANT: This must match the addon folder name
    bl_idname = "blendertools"

    auto_import_enabled = bpy.props.BoolProperty(
        name="Enable Auto Import",
        description="Automatically import templates at addon startup",
        default=True
    )

    additional_import_paths = bpy.props.CollectionProperty(
        type=addonprefs_props.TemplatePathItem,
        name="Additional Paths"
    )

    enable_armature = bpy.props.BoolProperty(name="Enable Armature Tools", default=True)
    enable_node_groups = bpy.props.BoolProperty(name="Enable Node Group Tools", default=True)
    enable_workflow = bpy.props.BoolProperty(name="Enable Workflows", default=True)
    enable_rpc_remote = bpy.props.BoolProperty(name="Enable RPC Remoting", default=False)
    enable_softbody = bpy.props.BoolProperty(name="Enable Softbody Tools", default=True)

    sbrebind_max_depth = bpy.props.IntProperty(name="Max Depth", default=48, min=0, max=1024)

    def draw(self, context):
        layout = self.layout

        # --- Enable Settings Box ---
        enable_box = layout.box()
        enable_box.label(text="Settings", icon="PREFERENCES")
        enable_box.prop(self, "enable_armature")
        enable_box.prop(self, "enable_node_groups")
        enable_box.prop(self, "enable_workflow")
        enable_box.prop(self, "enable_rpc_remote")
        enable_box.prop(self, "enable_softbody")

        # --- Additional Template Paths (Shown Only if Enabled) ---
        if self.enable_node_groups:
            box = layout.box()
            box.label(text="Node Group Tools Settings", icon="NODE")
            box.prop(self, "auto_import_enabled")    
            path_box = box.box()
            path_box.label(text="Additional Import Paths", icon="FILE_FOLDER")
            layout.operator("blendertools.add_template_path", icon="ADD")
            for idx, item in enumerate(self.additional_import_paths):
                row = path_box.row()
                row.prop(item, "path", text=f"Path {idx + 1}")
                op = row.operator("blendertools.remove_template_path", text="", icon="X")
                op.index = idx

        if self.enable_softbody:
            box = layout.box()
            box.label(text="Softbody Tools Settings", icon="PHYSICS")
            box.prop(self, "sbrebind_max_depth")


def register():
    bpy.utils.register_class(BlendertoolsAddonPreferences)


def unregister():
    bpy.utils.unregister_class(BlendertoolsAddonPreferences)
