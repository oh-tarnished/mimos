from fastapi import APIRouter, HTTPException, WebSocket
import app.models.models as models
import app.controllers.controllers as controllers

router = APIRouter()


@router.get("/animations", response_model=models.AnimationData)
def get_animation(animation_name: str):
    """
    This function is used to get the animation data from the config file.
    Using the animation name, it will search for the animation in the config file.
    If the animation is not found, it will return None with HTTP status code 404.

    Args:
        animation_name (str): animation name from the toml database.
    """
    res = controllers.get_animation(animation_name)
    if res is None:
        raise HTTPException(
            status_code=404, detail=f"animation '{animation_name}' not found"
        )

    return res


@router.websocket("/animations")
async def get_animations_ws(ws: WebSocket, animation_name: str):
    """
    This function is used to get frames from the animation. It will send the frames to the client using websocket.
    if aninmation is not found, it will return None with WS status code 1008

    Args:
        ws (WebSocket): websocket object.
        animation_name (str): animation name from the toml database.
    """
    await ws.accept()
    res = controllers.get_animation(animation_name)

    if res is None:
        await ws.close(code=1008, reason=f"animation '{animation_name}' not found")
        return

    # sending initial animation information (name, start_frame, end_frame)
    await ws.send_json(
        {
            "action": res.action,
            "start_frame": res.start_frame,
            "end_frame": res.end_frame,
        }
    )

    # sending the frames one by one
    for frame in res.frames:
        await ws.send_text(frame.json())
