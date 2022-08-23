from fastapi import FastAPI
import app.utils.config as config
import app.routes as routes

app = FastAPI(
    title="digital twin",
    version="0.1",
    docs_url=None if config.environment == "production" else "/docs",
)
app.include_router(routes.router)
