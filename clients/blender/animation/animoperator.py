# consists of Operator class, used to create a custom anim in blender
import os
import bpy
import sys
import json
import queue
import asyncio
import threading
import websockets

sys.path.insert(0, os.getcwd())
import utils as animutils


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

    def __init__(self):
        self.queue = queue.SimpleQueue()
        self.streaming_thread = None

    def modal(self, context, event):
        if event.type in {"ESC", "RIGHTMOUSE"}:
            self.cancel(context)
            return {"FINISHED"}
        if event.type == "TIMER":
            # for each time event, get the current frame data from websocket and apply to rig
            frame = self.queue.get()
            if frame is None:
                return {"FINISHED"}

            for joint_name, angle in frame["angles"].items():
                animutils.run(joint_name, angle)
        return {"PASS_THROUGH"}

    def execute(self, context):
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
        async with websockets.connect(
            f"ws://localhost:8000/animations?animation_name={animation_name}"
        ) as ws:
            try:
                animation_info = json.loads(await ws.recv())
            except websockets.exceptions.ConnectionClosedError:
                queue.put_nowait(None)
                return
            for _ in range(animation_info["start_frame"], animation_info["end_frame"]):
                queue.put_nowait(json.loads(await ws.recv()))
            queue.put_nowait(None)

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)

    def __del__(self):
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
