import bpy

light_object = bpy.data.objects["Area"]
if not light_object:
    print("Could not find Light Object in Example File!")
    exit

light_object_data = light_object.data

light_object_data.energy = 1000

