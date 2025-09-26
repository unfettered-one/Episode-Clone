from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from apis.story_api import router as story_router
from apis.service_state import router as service_state_router

app = FastAPI(
    title="Episode Clone Service",
    description="API for Episode Clone",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# determine assets dir reliably (project-root/assets)
ASSETS_DIR = Path(__file__).resolve().parents[1] / "assets"
app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")

app.include_router(story_router)
app.include_router(service_state_router)
