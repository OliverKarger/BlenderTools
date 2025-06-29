import bpy

from . import utils


class BlenderTools_ArmatureSync_Check(bpy.types.Operator):
    bl_idname = "blendertools.armaturesync_check"
    bl_label = "Check Compatibility"

    def execute(self, context):
        props = context.scene.blendertools_armaturesync
        source = props.source_armature
        target = props.target_armature

        if not source or not target:
            self.report({"ERROR"}, "Please set Source and Target Armature!")
            return {"CANCELLED"}

        if source.type != "ARMATURE" or target.type != "ARMATURE":
            self.report({"ERROR"}, "Both objects must be of type 'ARMATURE'")
            return {"CANCELLED"}

        messages = []

        # --- Scale Checks ---
        def is_uniform_scale(obj):
            return all(abs(s - 1.0) < 1e-4 for s in obj.scale)

        if not is_uniform_scale(source):
            messages.append(
                f"Source Armature '{source.name}' has non-uniform scale: {tuple(round(s, 3) for s in source.scale)}"
            )

        if not is_uniform_scale(target):
            messages.append(
                f"Target Armature '{target.name}' has non-uniform scale: {tuple(round(s, 3) for s in target.scale)}"
            )

        # Relative scale difference
        scale_diff = tuple(round(ts - ss, 4) for ss, ts in zip(source.scale, target.scale))
        if any(abs(d) > 0.01 for d in scale_diff):
            messages.append(f"Significant scale difference between Source and Target: Δ = {scale_diff}")

        # --- Bone Comparison ---
        source_bones = {bone.name for bone in source.data.bones}
        target_bones = {bone.name for bone in target.data.bones}

        missing_in_target = source_bones - target_bones
        missing_in_source = target_bones - source_bones

        messages.append(f"Bone Count: Source = {len(source_bones)}, Target = {len(target_bones)}")

        if missing_in_target:
            messages.append(
                f"{len(missing_in_target)} bone(s) missing in Target: {', '.join(sorted(missing_in_target)[:5])}..."
            )

        if missing_in_source:
            messages.append(
                f"{len(missing_in_source)} bone(s) missing in Source: {', '.join(sorted(missing_in_source)[:5])}..."
            )

        # --- Reporting ---
        if messages:
            for msg in messages:
                self.report({"INFO"}, msg)
        else:
            self.report({"INFO"}, "Armatures appear compatible.")

        return {"FINISHED"}


class BlenderTools_ArmatureSync_Enum(bpy.types.Operator):
    bl_idname = "blendertools.armaturesync_enum"
    bl_label = "Enumerate Bones"

    def execute(self, context):
        props = context.scene.blendertools_armaturesync
        source = props.source_armature
        target = props.target_armature

        if not source or not target:
            self.report({"ERROR"}, "Please set Source and Target Armature!")
            return {"CANCELLED"}

        if source.type != "ARMATURE" or target.type != "ARMATURE":
            self.report({"ERROR"}, "Both objects must be of type 'ARMATURE'")
            return {"CANCELLED"}

        props.bones.clear()

        source_bones = {bone for bone in source.data.bones}
        target_names = {bone.name for bone in target.data.bones}

        matching_bones: list[bpy.types.Bone] = [bone for bone in source_bones if bone.name in target_names]

        if not matching_bones:
            self.report({"WARNING"}, "No matching bones found between armatures.")
            return {"CANCELLED"}

        for bone in matching_bones:
            item = props.bones.add()
            item.name = bone.name
            item.linked_name = bone.name
            item.source_armature = source
            item.target_armature = target
            item.should_be_synced = True
            item.sync_enabled = False

            # Check which bone collection(s) this bone belongs to
            for collection in utils.get_bone_groups(source):
                if bone.name in collection.bones:
                    item.bone_group = collection.name
                    break

        self.report({"INFO"}, f"Found {len(matching_bones)} matching bones.")
        return {"FINISHED"}


class BlenderTools_ArmatureSync_Enable(bpy.types.Operator):
    bl_idname = "blendertools.armaturesync_enable"
    bl_label = "Enable Armature Sync"

    def invoke(self, context, event):
        props = context.scene.blendertools_armaturesync
        source = props.source_armature
        target = props.target_armature

        if not source or not target:
            self.report({"ERROR"}, "Please set Source and Target Armature!")
            return {"CANCELLED"}

        if utils.has_significant_scale_difference(source, target):
            return context.window_manager.invoke_props_dialog(self)

        return self.execute(context)

    def draw(self, context):
        props = context.scene.blendertools_armaturesync
        source = props.source_armature
        target = props.target_armature

        self.layout.label(text=f"Source Scale: {tuple(round(s, 3) for s in source.scale)}")
        self.layout.label(text=f"Target Scale: {tuple(round(s, 3) for s in target.scale)}")
        self.layout.prop(self, "CompensateScale")

    def execute(self, context):
        props = context.scene.blendertools_armaturesync
        bones = props.bones
        collection_filter = props.bone_collections

        if not props.bones:
            self.report({"ERROR"}, "No bones to sync. Please enumerate bones first.")
            return {"CANCELLED"}

        applied_count = 0

        filtered_bones = []
        if collection_filter == "ALL":
            filtered_bones += bones
        else:
            for bone in bones:
                if bone.bone_group == collection_filter:
                    filtered_bones.append(bone)

        for bone_data in filtered_bones:
            if not bone_data.should_be_synced:
                self.report({"DEBUG"}, f"Bone {bone_data.name} should not be synced. Skipping...")
                continue

            source = bone_data.source_armature
            target = bone_data.target_armature
            source_bone = bone_data.name
            target_bone = bone_data.linked_name

            if not source or not target or source.type != "ARMATURE" or target.type != "ARMATURE":
                self.report({"DEBUG"}, "Source or Target Armatures are not of Type Armature")
                continue
            if source_bone not in source.pose.bones or target_bone not in target.pose.bones:
                self.report(
                    {"DEBUG"},
                    f"Source Bone {source_bone.name} is not in Source Armature or Target Bone {target_bone.name} is not in Target Armature",  # noqa: E501
                )
                continue

            bpy.ops.object.mode_set(mode="OBJECT")
            bpy.context.view_layer.objects.active = target
            bpy.ops.object.mode_set(mode="POSE")

            pbone = target.pose.bones[target_bone]

            for con in list(pbone.constraints):
                if con.name == "ArmatureSync":
                    pbone.constraints.remove(con)

            con: bpy.types.CopyTransformsConstraint = pbone.constraints.new(type="COPY_TRANSFORMS")
            con.name = "ArmatureSync"
            con.target = source
            con.subtarget = source_bone
            con.mix_mode = props.constraint_mix_mode

            bone_data.sync_enabled = True
            applied_count += 1
            self.report({"DEBUG"}, f"Added Sync Constraint to Bone {bone_data.name}")

        self.report({"INFO"}, f"ync constraints applied to {applied_count} bones (target follows source).")
        return {"FINISHED"}


class BlenderTools_ArmatureSync_Disable(bpy.types.Operator):
    bl_idname = "blendertools.armaturesync_disable"
    bl_label = "Disable Armature Sync"

    def execute(self, context):
        props = context.scene.blendertools_armaturesync
        source = props.source_armature
        target = props.target_armature
        bones = props.bones
        collection_filter = props.bone_collections

        if not source or not target:
            self.report({"ERROR"}, "Please set Source and Target Armature!")
            return {"CANCELLED"}

        if target.type != "ARMATURE":
            self.report({"ERROR"}, "Target must be an Armature")
            return {"CANCELLED"}

        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.context.view_layer.objects.active = target
        bpy.ops.object.mode_set(mode="POSE")

        removed_count = 0

        filtered_bones = []
        if collection_filter == "ALL":
            filtered_bones += bones
        else:
            for bone in bones:
                if bone.bone_group == collection_filter:
                    filtered_bones.append(bone)

        for bone_data in filtered_bones:
            target_bone_name = bone_data.linked_name

            if not target_bone_name or target_bone_name not in target.pose.bones:
                continue

            pbone = target.pose.bones[target_bone_name]

            to_remove = [c for c in pbone.constraints if c.name == "ArmatureSync"]

            for c in to_remove:
                pbone.constraints.remove(c)
                removed_count += 1

            bone_data.sync_enabled = False
            self.report({"DEBUG"}, f"Sync Constraint removed from Bone {bone_data.name}")

        self.report({"INFO"}, f"Removed {removed_count} sync constraints from target rig.")
        return {"FINISHED"}


class BlenderTools_ArmatureSync_SetSource(bpy.types.Operator):
    bl_idname = "blendertools.armaturesync_setsource"
    bl_label = "Set as Source Armature"

    def execute(self, context):
        props = context.scene.blendertools_armaturesync
        props.source_armature = context.active_object
        self.report({"DEBUG"}, f"Object {context.active_object.name} set as Source Armature")
        return {"FINISHED"}


class BlenderTools_ArmatureSync_SetTarget(bpy.types.Operator):
    bl_idname = "blendertools.armaturesync_settarget"
    bl_label = "Set as Target Armature"

    def execute(self, context):
        props = context.scene.blendertools_armaturesync
        props.target_armature = context.active_object
        self.report({"DEBUG"}, f"Object {context.active_object.name} set as Target Armature")
        return {"FINISHED"}


def register():
    bpy.utils.register_class(BlenderTools_ArmatureSync_Enum)
    bpy.utils.register_class(BlenderTools_ArmatureSync_Enable)
    bpy.utils.register_class(BlenderTools_ArmatureSync_Disable)
    bpy.utils.register_class(BlenderTools_ArmatureSync_Check)
    bpy.utils.register_class(BlenderTools_ArmatureSync_SetSource)
    bpy.utils.register_class(BlenderTools_ArmatureSync_SetTarget)


def unregister():
    bpy.utils.unregister_class(BlenderTools_ArmatureSync_Enum)
    bpy.utils.unregister_class(BlenderTools_ArmatureSync_Enable)
    bpy.utils.unregister_class(BlenderTools_ArmatureSync_Disable)
    bpy.utils.unregister_class(BlenderTools_ArmatureSync_Check)
    bpy.utils.unregister_class(BlenderTools_ArmatureSync_SetSource)
    bpy.utils.unregister_class(BlenderTools_ArmatureSync_SetTarget)
