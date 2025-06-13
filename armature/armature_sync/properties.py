import bpy

from ...blender.constraint import CONSTRAINT_MIX_MODE


class BlenderTools_ArmatureSyncBone(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Bone Name")
    linked_name: bpy.props.StringProperty(name="Linked Bone Name")
    source_armature: bpy.props.PointerProperty(name="Source Armature", type=bpy.types.Object)
    target_armature: bpy.props.PointerProperty(name="Target Armature", type=bpy.types.Object)
    sync_enabled: bpy.props.BoolProperty(name="Is synced")
    should_be_synced: bpy.props.BoolProperty(name="Should be synced")


class BlenderTools_ArmatureSyncProps(bpy.types.PropertyGroup):
    source_armature: bpy.props.PointerProperty(name="Source Armature", type=bpy.types.Object)
    target_armature: bpy.props.PointerProperty(name="Target Armature", type=bpy.types.Object)
    bones: bpy.props.CollectionProperty(type=BlenderTools_ArmatureSyncBone)
    active_bone_index: bpy.props.IntProperty(name="Active Bone Index")
    constraint_mix_mode: bpy.props.EnumProperty(name="Mix", items=CONSTRAINT_MIX_MODE)


def register():
    bpy.utils.register_class(BlenderTools_ArmatureSyncBone)
    bpy.utils.register_class(BlenderTools_ArmatureSyncProps)

    bpy.types.Scene.blendertools_armaturesync = bpy.props.PointerProperty(type=BlenderTools_ArmatureSyncProps)


def unregister():
    bpy.utils.unregister_class(BlenderTools_ArmatureSyncProps)
    bpy.utils.unregister_class(BlenderTools_ArmatureSyncBone)

    del bpy.types.Scene.blendertools_armaturesync
