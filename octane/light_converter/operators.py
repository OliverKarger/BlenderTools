import bpy

class BlenderTools_OT_convert_lightsource_to_octane(bpy.types.Operator):
    bl_idname = "blendertools.convert_lightsource_to_octane"
    bl_label = "Convert to Octane Light"

    def execute(self, context):

        if context.scene.render.engine != 'octane':
            self.report({"ERROR"}, "Please set Render Engine to Octane!")
            return {"CANCELLED"}

        obj = context.object
        if obj is None or obj.type != "LIGHT":
            self.report({"ERROR"}, "Selected Object is not a Light!")
            return {"CANCELLED"}

        light_data = obj.data
        light_type = light_data.type

        # Create a new light datablock
        new_light_data = bpy.data.lights.new(name=f"OCTANE_{light_data.name}", type='AREA')

        # Set Octane-specific properties if available
        if hasattr(new_light_data, "octane"):
            if light_type == 'POINT':
                new_light_data.octane.light_type = '0'  # Point
            elif light_type == 'SUN':
                new_light_data.octane.light_type = '2'  # Directional
            elif light_type == 'AREA':
                new_light_data.octane.light_type = '1'  # Area
            elif light_type == 'SPOT':
                new_light_data.octane.light_type = '0'  # Treat as point for now
            else:
                self.report({"WARNING"}, f"Light type {light_type} not specifically handled.")

        # Create object using the new light datablock
        octane_light = bpy.data.objects.new(name=f"OCTANE_{obj.name}", object_data=new_light_data)
        context.collection.objects.link(octane_light)

        # Match transform
        octane_light.location = obj.location
        octane_light.rotation_euler = obj.rotation_euler
        octane_light.scale = obj.scale

        # Optionally hide the original light
        obj.hide_set(True)

        self.report({"INFO"}, f"Converted {obj.name} to Octane Light")
        return {"FINISHED"}

def register():
    bpy.utils.register_class(BlenderTools_OT_convert_lightsource_to_octane)

def unregister():
    bpy.utils.unregister_class(BlenderTools_OT_convert_lightsource_to_octane)