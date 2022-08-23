import os

os.environ["DIGITAL_TWIN_ENVIRONMENT"] = "production"

import uvicorn
from app import app

# run the application

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
