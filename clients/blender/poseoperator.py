import bpy
import json
import queue
import asyncio
from threading import Thread
import websockets


def initialize_blender(object: str):
    context = bpy.context
    obj = bpy.data.objects[object]
    bones = obj.pose.bones
    # set action to object
    # create the animation data if it doesn't exist
    if not obj.animation_data:
        obj.animation_data_create()
    return (context, obj, bones)


def apply_location(obj, bone: str, location: list):
    if bone in obj.pose.bones.keys():
        boneobj = obj.pose.bones[bone]
        boneobj.location = location
    else:
        print(f"Bone {bone} not found in {obj}")


def run(obj_name, joint_name: str, joint_angle: list):
    initialize_blender(obj_name)
    obj = bpy.data.objects[obj_name]
    apply_location(obj, joint_name, joint_angle)


face_obj = bpy.data.objects["Stewart Platform"]


class PoseMimicOperator(bpy.types.Operator):
    bl_idname = "object.pose_mimic_operator"
    bl_label = "Pose Mimic Operator"

    def __init__(self):
        self.queue = queue.SimpleQueue()
        self.streaming_thread = None

    def modal(self, context, event):
        if event.type == "TIMER":
            frame = self.queue.get()

            if frame is None:
                return {"FINISHED"}
            else:
                frame_number = frame["frame_number"]
                print("frame number::", frame_number)

                offsets = frame["offsets"][0]
                for joint_name, loc_array in offsets.items():
                    # joint_name, loc_array = joint
                    ## scale values bw 0.001 to -0.001
                    scaled_loc_array = [(0.02 * loc - 0.01) for loc in loc_array]
                    run("Stewart Platform", joint_name, scaled_loc_array)
        return {"PASS_THROUGH"}

    def execute(self, context):
        print("execute.....")
        wm = context.window_manager
        # adding timer event for step of 0.04 secs
        self._timer = wm.event_timer_add(time_step=0.04, window=context.window)
        wm.modal_handler_add(self)
        self.streaming_thread = Thread(
            target=asyncio.run,
            args=[PoseMimicOperator.get_pose(self.queue, "head_pose2new")],
        )
        self.streaming_thread.start()
        return {"RUNNING_MODAL"}

    # get frame data for requested animation
    async def get_pose(queue, tomlfile: str):
        """
        This function is used to get the frame data for the animation websocket.
        It will add the frame data to the queue.
        It will run until the queue is empty.

        Args:
            queue (_type_): queue.
            animation_name (_type_): animation name.
        """
        async with websockets.connect(
            f"ws://localhost:8000/pose?tomlfile={tomlfile}.toml"  # ?animation_name={animation_name}"
        ) as ws:
            try:
                animation_info = json.loads(await ws.recv())
                print("animation info", animation_info)
                for _ in range(
                    animation_info["start_frame"], animation_info["end_frame"]
                ):  # animation_info["end_frame"]
                    queue.put(json.loads(await ws.recv()))
            except websockets.exceptions.ConnectionClosedError:
                queue.put_nowait(None)
                return

            queue.put_nowait(None)

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)

    def __del__(self):
        print("delete...")
        if self.streaming_thread:
            self.streaming_thread.join()


def register():
    bpy.utils.register_class(PoseMimicOperator)


def unregister():
    bpy.utils.unregister_class(PoseMimicOperator)


register()
# bpy.types.VIEW3D_MT_object.append(menu_func)
bpy.ops.object.pose_mimic_operator()
