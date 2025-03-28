from fastapi import APIRouter, FastAPI

from app import config
from app.routes.auth import router as auth_router

app = FastAPI(debug=config.DEBUG)
router = APIRouter(prefix="/api/v1")


@router.get(
    "/ping",
    tags=["Utility"],
    description="Check if the server is running.",
)
async def ping():
    return {"msg": "pong"}


router.include_router(auth_router)
app.include_router(router)
