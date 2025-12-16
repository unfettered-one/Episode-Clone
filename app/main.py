from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

from apis.story_api import router as story_router
from apis.service_state import router as service_state_router

from errorhub.exceptions import ErrorHubException
from mangum import Mangum

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

mangum_handler = Mangum(app)


# Global Exception Handler
@app.exception_handler(ErrorHubException)
async def errorhub_exception_handler(request: Request, exc: ErrorHubException):
    """
    Catch all ErrorHubExceptions and return structured JSON response.
    The FastAPI exception handler receives the request as the first
    positional argument and the exception as the second.
    """
    return JSONResponse(status_code=exc.error_detail.code, content=exc.to_dict())
