import bpy


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


def apply_angle(obj, bone: str, joint_angle: list):
    """
    This function is used to apply the angle to the bone.
    Args:
        obj (_type_): blender object.
        bone (str): bone name.
        joint_angle (list): list of euler angles.
    """
    if bone in obj.pose.bones.keys():
        boneobj = obj.pose.bones[bone]
        boneobj.rotation_euler = joint_angle
    else:
        print(f"Bone {bone} not found in {obj}")


def run(joint_name: str, joint_angle: list):
    """
    Helper function that combines initialize_blender and apply_angle.
    Args:
        joint_name (str): joint name.
        joint_angle (list): list of euler angles.
    """
    initialize_blender("BODY_Bones")
    obj = bpy.data.objects["BODY_Bones"]
    apply_angle(obj, joint_name, joint_angle)
