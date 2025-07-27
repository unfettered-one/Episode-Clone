from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/info")
async def read_info():
    return JSONResponse(status_code=200, content={"message": "Welcome to the Episode Clone API!"})
