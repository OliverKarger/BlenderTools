import bpy
import bmesh

MODIFIERS_TO_REMOVE = []  # e.g. ["SUBSURF", "SOLIDIFY", "MIRROR"]


def apply_decimate_modifier(obj, ratio):
    mod = obj.modifiers.new(name="Decimate", type="DECIMATE")
    mod.ratio = ratio
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier=mod.name)


def remove_unwanted_modifiers(obj):
    for mod in list(obj.modifiers):
        if mod.type in MODIFIERS_TO_REMOVE:
            obj.modifiers.remove(mod)


def create_vertex_group_from_selection(obj, group_name):
    mesh = bmesh.from_edit_mesh(obj.data)
    selected_verts = [v.index for v in mesh.verts if v.select]

    vg = obj.vertex_groups.new(name=group_name)
    bpy.ops.object.mode_set(mode="OBJECT")
    vg.add(selected_verts, 1.0, "REPLACE")
    bpy.ops.object.mode_set(mode="EDIT")
    return vg.name


def finalize_proxy(proxy, source_obj, context, operator_self, sim_type):
    # Clean
    proxy.data.materials.clear()
    remove_unwanted_modifiers(proxy)

    # Decimate
    apply_decimate_modifier(proxy, operator_self.decimate_factor)

    # Simulation modifier
    proxy.modifiers.new(name=f"{sim_type}_Sim", type=sim_type)

    # Visibility
    proxy.hide_render = operator_self.hide_render
    proxy.hide_viewport = operator_self.hide_viewport

    # Parenting
    if operator_self.parent:
        proxy.parent = source_obj


def add_deform_modifiers_to_base(obj, proxy, group_name=None):
    import bpy

    # Add Surface Deform modifier
    deform = obj.modifiers.new(name="SurfaceDeform", type="SURFACE_DEFORM")
    deform.target = proxy
    if group_name:
        deform.vertex_group = group_name

    # Add Corrective Smooth with Smooth Type
    cs_modifier = obj.modifiers.new(name="CorrectiveSmooth", type="CORRECTIVE_SMOOTH")
    cs_modifier.smooth_type = "LENGTH_WEIGHTED"

    # Prepare selection and context
    bpy.ops.object.select_all(action="DESELECT")
    proxy.select_set(True)
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    # Attempt to bind Surface Deform
    try:
        bpy.ops.object.surfacedeform_bind(modifier=deform.name)
    except RuntimeError as e:
        print(f"Initial bind failed: {e}")
        if "concave polygons" in str(e).lower():
            # Add triangulate modifier and apply it
            tri_mod = obj.modifiers.new(name="TriangulateFix", type="TRIANGULATE")
            bpy.ops.object.modifier_apply(modifier=tri_mod.name)
            print("Applied Triangulate modifier to fix concave polygons")

            # Retry binding
            try:
                bpy.ops.object.surfacedeform_bind(modifier=deform.name)
            except RuntimeError as e2:
                print(f"Retry bind failed: {e2}")
        else:
            print("Unhandled Surface Deform bind error.")


def generate_proxy(context, operator_self, sim_type):
    mode = context.object.mode
    obj = context.active_object if mode == "OBJECT" else context.edit_object
    vg_name = None

    if not obj or obj.type != "MESH":
        operator_self.report({"ERROR"}, "Please select a Mesh Object!")
        return None, None

    if mode == "OBJECT":
        bpy.ops.object.select_all(action="DESELECT")
        obj.select_set(True)
        context.view_layer.objects.active = obj
        bpy.ops.object.duplicate()
        proxy = context.active_object

    elif mode == "EDIT":
        mesh = bmesh.from_edit_mesh(obj.data)
        if not any(v.select for v in mesh.verts):
            operator_self.report({"ERROR"}, "Please select Vertices!")
            return None, None

        vg_name = f"{sim_type.title()}_ProxyDeform"
        vg_name = create_vertex_group_from_selection(obj, vg_name)

        bpy.ops.mesh.duplicate()
        bpy.ops.mesh.separate(type="SELECTED")
        bpy.ops.object.mode_set(mode="OBJECT")

        proxy = [o for o in context.selected_objects if o != obj][-1]

    else:
        operator_self.report({"ERROR"}, "Unsupported mode!")
        return None, None

    finalize_proxy(proxy, obj, context, operator_self, sim_type)
    add_deform_modifiers_to_base(obj, proxy, vg_name if mode == "EDIT" else None)
    return obj, proxy
