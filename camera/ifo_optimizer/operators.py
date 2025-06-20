import bpy

from ..utils.camera_view import get_objects_in_camera_view


class BlenderTools_IfoOptimizer_HideObjects(bpy.types.Operator):
    bl_idname = "blendertools.ifooptimizer_hideobjects"
    bl_label = "Hide Objects not visible in Camera View"

    Include_Meshes: bpy.props.BoolProperty(name="Include Meshes", default=True)
    Include_Lights: bpy.props.BoolProperty(name="Include Lights", default=False)
    Include_LightProbes: bpy.props.BoolProperty(name="Include Light Probes", default=False)
    Include_Cameras: bpy.props.BoolProperty(name="Include Cameras", default=False)
    Include_Curves: bpy.props.BoolProperty(name="Include Curves", default=True)
    Include_Empties: bpy.props.BoolProperty(name="Include Empties", default=True)
    Include_Armatures: bpy.props.BoolProperty(name="Include Armatures", default=True)
    Include_Lattices: bpy.props.BoolProperty(name="Include Lattices", default=True)
    Include_Metas: bpy.props.BoolProperty(name="Include Metas", default=True)
    Include_Fonts: bpy.props.BoolProperty(name="Include Fonts", default=True)
    Include_Speakers: bpy.props.BoolProperty(name="Include Speakers", default=True)
    Include_Volumes: bpy.props.BoolProperty(name="Include Volumess", default=True)

    def draw(self, context):
        layout = self.layout

        layout.prop(self, "Include_Meshes")
        layout.prop(self, "Include_Lights")
        layout.prop(self, "Include_LightProbes")
        layout.prop(self, "Include_Cameras")
        layout.prop(self, "Include_Curves")
        layout.prop(self, "Include_Empties")
        layout.prop(self, "Include_Armatures")
        layout.prop(self, "Include_Lattices")
        layout.prop(self, "Include_Metas")
        layout.prop(self, "Include_Fonts")
        layout.prop(self, "Include_Speakers")
        layout.prop(self, "Include_Volumes")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        props = context.scene.blendertools_ifooptimizer
        addon = context.preferences.addons.get("blendertools")

        if addon.preferences.settings.viewport_selector_enabled:
            cam = context.active_object
        else:
            cam = props.camera

        if not cam and cam.type != "CAMERA":
            self.report({"ERROR"}, "Please select a Camera")
            return {"CANCELLED"}

        include_map = {
            "MESH": self.Include_Meshes,
            "LIGHT": self.Include_Lights,
            "LIGHT_PROBE": self.Include_LightProbes,
            "CAMERA": self.Include_Cameras,
            "CURVE": self.Include_Curves,
            "EMPTY": self.Include_Empties,
            "ARMATURE": self.Include_Armatures,
            "LATTICE": self.Include_Lattices,
            "META": self.Include_Metas,
            "FONT": self.Include_Fonts,
            "SPEAKER": self.Include_Speakers,
            "VOLUME": self.Include_Volumes,
        }

        allowed_types = {k for k, v in include_map.items() if v}

        if not props.hidden_objects or len(props.hidden_objects) == 0:
            in_view = set(get_objects_in_camera_view(context, cam))

            all_objects = {obj for obj in context.visible_objects if obj.type in allowed_types and obj != cam}

            objects_to_hide = list(all_objects - in_view)

            for obj in objects_to_hide:
                item = props.hidden_objects.add()
                item.name = obj.name
                item.hidden_viewport = obj.hide_get()
                item.disabled_viewport = obj.hide_viewport
                item.hidden_render = obj.hide_render
                item.object_type = obj.type

        for item in props.hidden_objects:
            if item.object_type not in allowed_types:
                continue

            obj = bpy.data.objects.get(item.name)
            if obj and obj != cam:
                obj.hide_set(True)
                obj.hide_render = True
                obj.hide_viewport = True
                self.report({"DEBUG"}, f"Hiding Object {item.name}")

        self.report({"INFO"}, f"Hidden {len(objects_to_hide)} Objects")
        return {"FINISHED"}


class BlenderTools_IfoOptimizer_ShowObjects(bpy.types.Operator):
    bl_idname = "blendertools.ifooptimizer_showobjects"
    bl_label = "Show Objects not visible in Camera View"

    def execute(self, context):
        props = context.scene.blendertools_ifooptimizer

        restored_objects = 0

        for i in reversed(range(len(props.hidden_objects))):
            item = props.hidden_objects[i]
            obj = bpy.data.objects.get(item.name)
            if obj:
                obj.hide_set(item.hidden_viewport)
                obj.hide_viewport = item.disabled_viewport
                obj.hide_render = item.hidden_render
                self.report({"DEBUG"}, "Restoring Object {item.name}")

            props.hidden_objects.remove(i)
            restored_objects += 1

        self.report({"INFO"}, f"Restored {restored_objects}")
        return {"FINISHED"}


def register():
    bpy.utils.register_class(BlenderTools_IfoOptimizer_HideObjects)
    bpy.utils.register_class(BlenderTools_IfoOptimizer_ShowObjects)


def unregister():
    bpy.utils.unregister_class(BlenderTools_IfoOptimizer_HideObjects)
    bpy.utils.unregister_class(BlenderTools_IfoOptimizer_ShowObjects)
