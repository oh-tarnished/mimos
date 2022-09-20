import os
import bpy
import sys
import zmq
import json
import math
import string
import numpy as np

sys.path.insert(0, os.getcwd())
from calculate import get_angle


def initialize_blender(object: str):
    context = bpy.context
    obj = bpy.data.objects[object]
    bones = obj.pose.bones
    # set action to object
    # create the animation data if it doesn't exist
    if not obj.animation_data:
        obj.animation_data_create()
    return (context, obj, bones)


# R_Elbow => R_Wrist + R_Shoulder + R_Elbow
# R_Shoulder => Neck + R_Elbow + R_Shoulder
# L_Elbow => L_Wrist + L_Shoulder + L_Elbow
# L_Shoulder => Neck + L_Elbow + L_Shoulder


keypoint_joint_map = {
    "R_Shoulder": {
        "id": 2,
        "scale": -0.5,
        "axis": "x",
        "euler": ["neck", "R_Elbow", "R_Shoulder"],
    },
    "R_Elbow": {
        "id": 3,
        "scale": -0.5,
        "axis": "z",
        "euler": ["R_Shoulder", "R_Elbow", "R_Wrist"],
    },
    "R_Wrist": {"id": 4, "scale": -1, "axis": "x", "euler": []},
    "L_Shoulder": {
        "id": 5,
        "scale": -0.5,
        "axis": "x",
        "euler": ["neck", "L_Elbow", "L_Shoulder"],
    },
    "L_Elbow": {
        "id": 6,
        "scale": -0.5,
        "axis": "z",
        "euler": ["L_Shoulder", "L_Elbow", "L_Wrist"],
    },
    "L_Wrist": {"id": 7, "scale": -1, "axis": "x", "euler": []},
    "neck": {"id": 0, "scale": 1, "axis": "x", "euler": []},
}


# map face and body to values, for face its location, while for arm its rotation
body_object = bpy.data.objects["BODY_Bones"]
body_bones = [bone.name for bone in body_object.pose.bones]
face_object = bpy.data.objects["Stewart Platform"]
face_bones = [bone.name for bone in face_object.pose.bones]


def apply_location(bpy_obj_name: string, bone: str, location: list):
    initialize_blender(bpy_obj_name)
    obj = bpy.data.objects[bpy_obj_name]
    if bone in obj.pose.bones.keys():
        boneobj = obj.pose.bones[bone]
        scale_x, scale_y, scale_z = 1, 1, 1
        boneobj.location.x = location[0] * scale_x
        boneobj.location.y = location[1] * scale_y
        boneobj.location.z = location[2] * scale_z
    else:
        pass
        print(f"Bone {bone} not found in {obj}")


def apply_rotation(
    bpy_obj_name: string, bone: str, rotation_value: float, axis: string
):
    initialize_blender(bpy_obj_name)
    obj = bpy.data.objects[bpy_obj_name]
    axis_index = {"x": 0, "y": 1, "z": 2}
    joint_axis_index = axis_index[axis.lower()]
    scale = keypoint_joint_map[bone]["scale"]
    if bone in obj.pose.bones.keys():
        boneobj = obj.pose.bones[bone]
        boneobj.rotation_euler[joint_axis_index] = rotation_value * scale
    else:
        print(f"Bone {bone} not found in {obj}")


class PoseMimicOperator(bpy.types.Operator):
    bl_idname = "object.pose_mimic_operator"
    bl_label = "Pose Mimic Operator"

    def __init__(self):
        self.ctx = zmq.Context()
        self.keypoint_socket = self.ctx.socket(zmq.SUB)
        self.keypoint_socket.bind("tcp://*:5555")
        self.keypoint_socket.setsockopt_string(zmq.SUBSCRIBE, "")
        self.frame_count = 0
        self.prev_rotation_array = [0, 0, 0]

    def modal(self, context, event):
        if event.type == "TIMER":
            json_response = json.loads(self.keypoint_socket.recv_json())

            for joint_name, value_array in json_response.items():
                if joint_name in body_bones:
                    bpy_object = "BODY_Bones"
                    joint_info = keypoint_joint_map[joint_name]
                    joint_axis = joint_info["axis"]
                    # get relative keypoint values for the joint
                    if joint_name in {"R_Shoulder", "L_Shoulder", "R_Elbow", "L_Elbow"}:
                        kp1, kp2, kp3 = [
                            np.array(json_response[joint])
                            for joint in joint_info["euler"]
                        ]
                        rotation_value = (
                            0
                            if math.isnan(get_angle(kp1, kp2, kp3))
                            else get_angle(kp1, kp2, kp3)
                        )
                    else:
                        rotation_value = 0
                    apply_rotation(bpy_object, joint_name, rotation_value, joint_axis)

                elif joint_name in face_bones:
                    bpy_object = "Stewart Platform"
                    scaled_array = [(0.02 * loc - 0.01) for loc in value_array]
                    # changing only z axis
                    location_array = [0, 0, scaled_array[-1]]
                    apply_location(bpy_object, joint_name, location_array)
        return {"PASS_THROUGH"}

    def execute(self, context):
        print("execute.....")
        wm = context.window_manager
        # adding timer event for step of 0.04 secs
        self._timer = wm.event_timer_add(time_step=0.004, window=context.window)
        wm.modal_handler_add(self)
        return {"RUNNING_MODAL"}

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)

    def __del__(self):
        print("delete...")


def register():
    bpy.utils.register_class(PoseMimicOperator)


def unregister():
    bpy.utils.unregister_class(PoseMimicOperator)


register()
bpy.ops.object.pose_mimic_operator()
