import app.utils.config as config
import toml
import os
from typing import Optional
from app.models.models import AnimationData
from pydantic import parse_obj_as


def get_animation(animation_name: str) -> Optional[AnimationData]:
    """
    This function is used to get the animation data from the config file.

    Args:
        animation_name (str): animation name from the toml database.

    Returns:
        Optional[AnimationData]: returns the animation data if found. Otherwise returns None.
    """
    file_name = f"{animation_name}.toml"
    if file_name not in os.listdir(config.animations_dir):
        return None

    res = toml.load(os.path.join(config.animations_dir, file_name))
    return parse_obj_as(AnimationData, res)
