import bpy
import zmq
import json
import queue


def initialize_blender(object: str):
    context = bpy.context
    obj = bpy.data.objects[object]
    bones = obj.pose.bones
    # set action to object
    # create the animation data if it doesn't exist
    if not obj.animation_data:
        obj.animation_data_create()
    return (context, obj, bones)


# "upper_lid.R.DN", "upper_lid.L.DN" - multiply by -1
# "lip_Upper.L", "lip_Upper.R", "lip_Upper.C"  - multiply by +1
# "lip_lower.L", "lip_lower.R", "lip_lower.C" - multiply by -1
# "brow.R.out", "brow.R.in", "brow.C" - multiply by +1
# "lip_streach.R","lip_streach.L" - multiply by +1

negative_scale = [
    "lip_lower.L",
    "lip_lower.R",
    "lip_lower.C",
    "upper_lid.R.DN",
    "upper_lid.L.DN",
]


def apply_location(obj, bone: str, location: list):
    if bone in obj.pose.bones.keys():
        boneobj = obj.pose.bones[bone]
        scale_x, scale_y, scale_z = 1, 1, 1

        boneobj.location.x = location[0] * scale_x
        boneobj.location.y = location[1] * scale_y
        boneobj.location.z = location[2] * scale_z
    else:
        pass
        # print(f"Bone {bone} not found in {obj}")


def run(obj_name, joint_name: str, joint_angle: list):
    initialize_blender(obj_name)
    obj = bpy.data.objects[obj_name]
    apply_location(obj, joint_name, joint_angle)


class PoseMimicOperator(bpy.types.Operator):
    bl_idname = "object.pose_mimic_operator"
    bl_label = "Pose Mimic Operator"

    def __init__(self):
        # self.streaming_thread = None
        self.ctx = zmq.Context()
        self.keypoint_socket = self.ctx.socket(zmq.SUB)
        self.keypoint_socket.bind("tcp://*:5555")
        self.keypoint_socket.setsockopt_string(zmq.SUBSCRIBE, "")
        self.frame_count = 0

    def modal(self, context, event):
        if event.type == "TIMER":
            json_resp = json.loads(self.keypoint_socket.recv_json())
            # if json_resp:
            for joint_name, loc_array in json_resp.items():
                # scale values bw 0.001 to -0.001
                scaled_loc_array = [(0.02 * loc - 0.01) for loc in loc_array]
                # taking only z value
                run("Stewart Platform", joint_name, [0, 0, scaled_loc_array[-1]])
            # else:
            #     print("received quit message", json_resp)
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


# if __name__ == "__main__":
register()
bpy.ops.object.pose_mimic_operator()
