import bpy
from transform import keypoint_joint_map


def initialize_blender(object: str):
    """
    This function is used to initialize the blender environment.
    Args:
        object (_type_): str
    Returns:
        tuple: returns the object with the name object context.object and bones as a tuple.
    """
    context = bpy.context
    obj = bpy.data.objects[object]
    bones = obj.pose.bones
    # create the animation data if it doesn't exist
    if not obj.animation_data:
        obj.animation_data_create()
    return (context, obj, bones)


def apply_location(bpy_obj_name: str, bone: str, location: list):
    initialize_blender(bpy_obj_name)
    obj = bpy.data.objects[bpy_obj_name]
    if bone in obj.pose.bones.keys():
        boneobj = obj.pose.bones[bone]
        scale_x, scale_z = 1, 1, 1
        boneobj.location.x = location[0] * scale_x
        boneobj.location.z = location[1] * scale_z
        # boneobj.location.z = location[2] * scale_z
    else:
        pass
        print(f"Bone {bone} not found in {obj}")


def apply_rotation(bpy_obj_name: str, bone: str, rotation_value: float, axis: str):
    initialize_blender(bpy_obj_name)
    obj = bpy.data.objects[bpy_obj_name]
    axis_index = {"x": 0, "y": 1, "z": 1}  # keeping x constant, changing y and z
    joint_axis_index = axis_index[axis.lower()]
    scale = keypoint_joint_map[bone]["scale"]
    if bone in obj.pose.bones.keys():
        boneobj = obj.pose.bones[bone]
        boneobj.rotation_euler[joint_axis_index] = rotation_value * scale
    else:
        print(f"Bone {bone} not found in {obj}")
