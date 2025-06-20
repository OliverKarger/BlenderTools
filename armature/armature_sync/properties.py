import bpy

from ...blender.constraint import CONSTRAINT_MIX_MODE


def get_bone_collection_items(self, context):
    props = context.scene.blendertools_armaturesync
    armature = props.source_armature

    if not armature or armature.type != "ARMATURE":
        return []

    items = [("ALL", "All", "Show all Bones", 0)]
    for i, collection in enumerate(armature.data.collections, start=1):
        items.append((collection.name, collection.name, f"Bone Collection: {collection.name}", i))

    return items


class BlenderTools_ArmatureSync_Bone(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Bone Name")
    linked_name: bpy.props.StringProperty(name="Linked Bone Name")
    source_armature: bpy.props.PointerProperty(name="Source Armature", type=bpy.types.Object)
    target_armature: bpy.props.PointerProperty(name="Target Armature", type=bpy.types.Object)
    sync_enabled: bpy.props.BoolProperty(name="Is synced")
    should_be_synced: bpy.props.BoolProperty(name="Should be synced")
    bone_group: bpy.props.StringProperty(name="Bone Group")


class BlenderTools_ArmatureSyncProps(bpy.types.PropertyGroup):
    source_armature: bpy.props.PointerProperty(
        name="Source Armature", type=bpy.types.Object, poll=lambda self, obj: obj.type == "ARMATURE"
    )
    target_armature: bpy.props.PointerProperty(
        name="Target Armature", type=bpy.types.Object, poll=lambda self, obj: obj.type == "ARMATURE"
    )
    bones: bpy.props.CollectionProperty(type=BlenderTools_ArmatureSync_Bone)
    bone_collections: bpy.props.EnumProperty(name="Bone Collections", items=get_bone_collection_items)
    active_bone_index: bpy.props.IntProperty(name="Active Bone Index")
    constraint_mix_mode: bpy.props.EnumProperty(name="Mix", items=CONSTRAINT_MIX_MODE)  # noqa:F821


def register():
    bpy.utils.register_class(BlenderTools_ArmatureSync_Bone)
    bpy.utils.register_class(BlenderTools_ArmatureSyncProps)

    bpy.types.Scene.blendertools_armaturesync = bpy.props.PointerProperty(type=BlenderTools_ArmatureSyncProps)


def unregister():
    bpy.utils.unregister_class(BlenderTools_ArmatureSyncProps)
    bpy.utils.unregister_class(BlenderTools_ArmatureSync_Bone)

    del bpy.types.Scene.blendertools_armaturesync
