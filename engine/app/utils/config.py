import os
from dotenv import load_dotenv, find_dotenv


# Load environment variables from .env file
load_dotenv(find_dotenv())
animations_dir = os.getenv("DIGITAL_TWIN_ANIMATION_DIR") or "animations"
environment = os.getenv("DIGITAL_TWIN_ENVIRONMENT") or "development"
