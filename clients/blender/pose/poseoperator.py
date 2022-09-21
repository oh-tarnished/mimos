import os
import bpy
import sys
import zmq
import json
import math
import string
import numpy as np

sys.path.insert(0, os.getcwd())
from transform import get_angle, keypoint_joint_map
from poseutils import apply_location, apply_rotation

# map face and body to values, for face its location, while for arm its rotation
body_object = bpy.data.objects["BODY_Bones"]
body_bones = [bone.name for bone in body_object.pose.bones]
face_object = bpy.data.objects["Stewart Platform"]
face_bones = [bone.name for bone in face_object.pose.bones]


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
                    location_array = [(0.02 * loc - 0.01) for loc in value_array[:2]]
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
