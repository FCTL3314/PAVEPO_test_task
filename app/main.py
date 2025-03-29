from fastapi import APIRouter, FastAPI

from app import settings
from app.routes.auth import router as auth_router
from app.routes.media import router as media_router
from lifespan import on_startup

app = FastAPI(debug=settings.DEBUG, on_startup=(on_startup,))
router = APIRouter(prefix="/api/v1")


@router.get(
    "/ping",
    tags=["Utility"],
    description="Check if the server is running.",
)
async def ping():
    return {"msg": "pong"}


router.include_router(auth_router)
router.include_router(media_router)
app.include_router(router)
