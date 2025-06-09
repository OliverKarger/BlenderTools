import bpy

class BlenderTools_ArmatureSyncBone(bpy.types.PropertyGroup):
    """Contains Information about a Bone"""

    Name: bpy.props.StringProperty(name="Bone Name")
    LinkedName: bpy.props.StringProperty(name="Linked Bone Name")
    SourceArmature: bpy.props.PointerProperty(name="Source Armature", type=bpy.types.Object)
    TargetArmature: bpy.props.PointerProperty(name="Target Armature", type=bpy.types.Object)
    SyncEnabled: bpy.props.BoolProperty(name="Is synced")
    ShouldBeSynced: bpy.props.BoolProperty(name="Should be synced")

class BlenderTools_ArmatureSyncProps(bpy.types.PropertyGroup):
    """ Contains Data for Armature Sync 
        This class is only used for the UI!
    """

    SourceArmature: bpy.props.PointerProperty(name="Source Armature", type=bpy.types.Object)
    TargetArmature: bpy.props.PointerProperty(name="Target Armature", type=bpy.types.Object)
    Bones: bpy.props.CollectionProperty(type=BlenderTools_ArmatureSyncBone)
    ActiveBoneIndex: bpy.props.IntProperty(name="Active Bone Index")

def register():
    print("Registering Armature Sync Properties")
    bpy.utils.register_class(BlenderTools_ArmatureSyncBone)
    bpy.utils.register_class(BlenderTools_ArmatureSyncProps)

    bpy.types.Scene.blendertools_armaturesync = bpy.props.PointerProperty(type=BlenderTools_ArmatureSyncProps)

def unregister():
    print("Unregistering Armature Sync Properties")
    bpy.utils.unregister_class(BlenderTools_ArmatureSyncProps)
    bpy.utils.unregister_class(BlenderTools_ArmatureSyncBone)
    
    del bpy.types.Scene.blendertools_armaturesync