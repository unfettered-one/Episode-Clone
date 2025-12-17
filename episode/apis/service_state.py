from fastapi import APIRouter, Security
from fastapi.responses import JSONResponse

from app.security.auth import verify_access_token

router = APIRouter()


@router.get("/info")
async def read_info(token_data=Security(verify_access_token)):
    return JSONResponse(status_code=200, content={"message": "Welcome to the Episode Clone API!"})
