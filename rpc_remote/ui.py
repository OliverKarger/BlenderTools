import bpy


class VIEW3D_PT_rpc_remote(bpy.types.Panel):
    bl_label = "RPC Remote"
    bl_idname = "VIEW3D_PT_rpc_remote"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Blender Tools"

    @classmethod
    def poll(cls, context):
        addon = context.preferences.addons.get("blendertools")
        if addon:
            return addon.preferences.enable_rpc_remote
        else:
            return False

    def draw(self, context):
        layout = self.layout

        props = context.scene.blendertools_rpcremote

        box = layout.box()
        box.label(text="Settings")
        box.prop(props, "ip")
        box.prop(props, "port")

        box.operator("blendertools.rpcremote_checkaddress")

        box = layout.box()
        box.label(text="Controls")

        if props.is_active:
            box.alert = True
            box.operator("blendertools.rpcremote_startserver", text="Server running")
        else:
            box.operator("blendertools.rpcremote_startserver")

        box.alert = False
        box.operator("blendertools.rpcremote_stopserver")


def register():
    bpy.utils.register_class(VIEW3D_PT_rpc_remote)


def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_rpc_remote)
