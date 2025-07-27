from fastapi import FastAPI

from apis.story_api import router as story_router
from apis.service_state import router as service_state_router

app = FastAPI(
    title="Episode Clone Service",
    description="API for Episode Clone",
    version="1.0.0",
)

app.include_router(story_router)
app.include_router(service_state_router)
