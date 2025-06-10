import bpy

class BlenderTools_SBRebindRecursive(bpy.types.Operator):
    """Recursively rebind all Surface/Mesh Deform Modifiers on children of the active object"""
    bl_idname = "blendertools.sbrebindrecursive"
    bl_label = "Rebind Softbody"

    def execute(self, context):
            active_obj = context.active_object

            addon = context.preferences.addons.get("blendertools")
            max_depth = addon.preferences.sbrebind_max_depth

            if not active_obj:
                self.report({'WARNING'}, "No active object selected.")
                return {'CANCELLED'}

            def rebind_modifier(mod, obj):
                if mod.type == 'MESH_DEFORM':
                    try:
                        bpy.ops.object.modifier_bind({'object': obj}, modifier=mod.name)
                        self.report({'INFO'}, f"Rebound Mesh Deform on {obj.name}")
                    except Exception as e:
                        self.report({'WARNING'}, f"Failed to bind Mesh Deform on {obj.name}: {e}")
                elif mod.type == 'SURFACE_DEFORM':
                    try:
                        bpy.ops.object.surfacedeform_bind({'object': obj}, modifier=mod.name)
                        self.report({'INFO'}, f"Rebound Surface Deform on {obj.name}")
                    except Exception as e:
                        self.report({'WARNING'}, f"Failed to bind Surface Deform on {obj.name}: {e}")

            def process_object(obj):
                for mod in obj.modifiers:
                    if mod.type in {'MESH_DEFORM', 'SURFACE_DEFORM'}:
                        mod.is_bind = False  # Unbind
                        rebind_modifier(mod, obj)

            def recurse_children(parent, depth):
                if depth > max_depth:
                    return
                for child in parent.children:
                    process_object(child)
                    recurse_children(child, depth + 1)

            recurse_children(active_obj, depth=1)

            return {'FINISHED'}
    
def register():
    print("Registering Softbody Rebind Operators")
    bpy.utils.register_class(BlenderTools_SBRebindRecursive)

def unregister():
    print("Unregistering Softbody Rebind Operators")
    bpy.utils.unregister_class(BlenderTools_SBRebindRecursive)