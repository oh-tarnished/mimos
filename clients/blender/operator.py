# consists of Operator class, used to create a custom anim in blender
import bpy
import sys
import json
import queue
import asyncio
import threading
import websockets


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
    # set action to object
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
    This function is used to run the animation.
    It will apply the angle to the bone.


    Args:
        joint_name (str): joint name.
        joint_angle (list): list of euler angles.
    """
    initialize_blender("BODY_Bones")
    obj = bpy.data.objects["BODY_Bones"]
    apply_angle(obj, joint_name, joint_angle)


class AnimationOperator(bpy.types.Operator):
    """
    This class is used to create and operate the animation in blender.
    """

    bl_idname = "object.animation_operator"
    bl_label = "Simple Animation Operator"

    animation_name: bpy.props.StringProperty(
        name="Enter the animation", default="sample-animation"
    )
    joint_name: bpy.props.StringProperty(name="Enter the joint name")
    frame: bpy.props.IntProperty(name="Enter the number of frames", default=1)

    # create thread and add get_frame method
    def __init__(self):
        self.queue = queue.SimpleQueue()
        self.streaming_thread = None

    def modal(self, context, event):
        """
        This operator defines a Operator.modal function that will keep being run to handle events until it returns {'FINISHED'} or {'CANCELLED'}.

        Args:
            context (_type_): blender context.
            event (_type_): blender event.

        Returns:
            _type_: returns  {'FINISHED'} or {'CANCELLED'} or {'PASS_THROUGH'} or {'INTERFACE'} or {'RUNNING_MODAL'}.
        """
        if event.type in {"ESC", "RIGHTMOUSE"}:
            self.cancel(context)
            return {"FINISHED"}
        if event.type == "TIMER":
            # for each time event, get the current frame data from websocket and apply to rig
            frame = self.queue.get()
            if frame is None:
                return {"FINISHED"}

            for joint_name, angle in frame["angles"].items():
                run(joint_name, angle)
        return {"PASS_THROUGH"}

    # executes operator
    def execute(self, context):
        """
        This function is used to execute the operator.

        Args:
            context (_type_): blender context.

        Returns:
            _type_: returns  {'FINISHED'} or {'CANCELLED'} or {'PASS_THROUGH'} or {'INTERFACE'} or {'RUNNING_MODAL'}.

        """
        message = "Popup Values: '%s' '%s' '%d'" % (
            self.animation_name,
            self.joint_name,
            self.frame,
        )
        self.report({"INFO"}, message)
        wm = context.window_manager
        # adding timer event for step of 0.04 secs
        self._timer = wm.event_timer_add(time_step=0.04, window=context.window)
        wm.modal_handler_add(self)
        animation_name = sys.argv[-1]
        self.streaming_thread = threading.Thread(
            target=asyncio.run,
            args=[AnimationOperator.get_frames(self.queue, animation_name)],
        )
        self.streaming_thread.start()
        return {"RUNNING_MODAL"}

    # get frame data for requested animation
    async def get_frames(queue, animation_name: str):
        """
        This function is used to get the frame data for the animation websocket.
        It will add the frame data to the queue.
        It will run until the queue is empty.

        Args:
            queue (_type_): queue.
            animation_name (_type_): animation name.
        """
        async with websockets.connect(f"ws://localhost:8000/pose") as ws:
            try:
                animation_info = json.loads(await ws.recv())
            except websockets.exceptions.ConnectionClosedError:
                queue.put_nowait(None)
                return
            for _ in range(animation_info["start_frame"], animation_info["end_frame"]):
                queue.put_nowait(json.loads(await ws.recv()))
            queue.put_nowait(None)

    def cancel(self, context):
        """
        This function is used to cancel the operator.

        Args:
            context (_type_): blender context.
        """
        wm = context.window_manager
        wm.event_timer_remove(self._timer)

    def __del__(self):
        """
        This function is used to delete the operator.
        """
        if self.streaming_thread:
            self.streaming_thread.join()


# Only needed if you want to add into a dynamic menu.
def menu_func(self, context):
    """
    This function is used to add the operator to the menu.

    Args:
        context (_type_): blender context.
    """
    self.layout.operator(AnimationOperator.bl_idname, text="Animation Operator")


def register():
    """This function is used to register the operator."""
    bpy.utils.register_class(AnimationOperator)


def unregister():
    """This function is used to unregister the operator."""
    bpy.utils.unregister_class(AnimationOperator)


register()
bpy.types.VIEW3D_MT_object.append(menu_func)
bpy.ops.object.animation_operator()
