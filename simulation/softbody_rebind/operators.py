import bpy


class BlenderTools_SoftbodyRebind_Rebind(bpy.types.Operator):

    bl_idname = "blendertools.softbodyrebind_rebind"
    bl_label = "Rebind Softbody"

    def execute(self, context):
        active_obj = context.active_object

        addon_prefs = context.preferences.addons.get("blendertools")
        if addon_prefs and hasattr(addon_prefs, "preferences"):
            max_depth = getattr(addon_prefs.preferences, "sbrebind_max_depth", 0)
        else:
            self.report({"WARNING"}, "Unable to find max_depth setting in addon preferences.")
            return {"CANCELLED"}

        if not active_obj:
            self.report({"WARNING"}, "No active object selected.")
            return {"CANCELLED"}

        def rebind_modifier(mod, obj):
            original_active = bpy.context.view_layer.objects.active
            current_mode = bpy.context.object.mode if bpy.context.object else "OBJECT"

            try:
                bpy.ops.object.mode_set(mode="OBJECT")
                bpy.ops.object.select_all(action="DESELECT")
                obj.select_set(True)
                bpy.context.view_layer.objects.active = obj

                if mod.type == "MESH_DEFORM":
                    bpy.ops.object.modifier_bind(modifier=mod.name)
                    self.report({"INFO"}, f"Rebound Mesh Deform on {obj.name}")
                elif mod.type == "SURFACE_DEFORM":
                    bpy.ops.object.surfacedeform_bind(modifier=mod.name)
                    self.report({"INFO"}, f"Rebound Surface Deform on {obj.name}")

            except Exception as e:
                self.report({"WARNING"}, f"Failed to bind {mod.type} on {obj.name}: {e}")

            finally:
                bpy.ops.object.select_all(action="DESELECT")
                if original_active:
                    original_active.select_set(True)
                    bpy.context.view_layer.objects.active = original_active
                if bpy.context.object:
                    bpy.ops.object.mode_set(mode=current_mode)

        def process_object(obj):
            for mod in obj.modifiers:
                if mod.type in {"MESH_DEFORM", "SURFACE_DEFORM"}:
                    rebind_modifier(mod, obj)

        def recurse_children(parent, depth):
            if depth > max_depth:
                return
            for child in parent.children:
                process_object(child)
                recurse_children(child, depth + 1)

        recurse_children(active_obj, depth=1)

        return {"FINISHED"}


def register():
    bpy.utils.register_class(BlenderTools_SoftbodyRebind_Rebind)


def unregister():
    bpy.utils.unregister_class(BlenderTools_SoftbodyRebind_Rebind)
