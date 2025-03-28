from fastapi import APIRouter, FastAPI

from app import config

app = FastAPI(debug=config.DEBUG)
router = APIRouter(prefix="/api/v1")


@router.get(
    "/ping",
    tags=["Utility"],
    description="Check if the server is running.",
)
async def ping():
    return {"msg": "pong"}


app.include_router(router)
