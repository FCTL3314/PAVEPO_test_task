from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Header
from httpx import HTTPStatusError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse

from app.dependencies import SessionDep
from app.repository.auth import get_or_create_user_by_yandex_user
from app.schemas.auth import AuthTokens, User as UserSchema
from app.services.auth import (
    create_access_token,
    create_refresh_token,
    get_current_user,
)
from app.services.yandex import (
    get_yandex_oauth_url,
    get_yandex_user,
    get_yandex_token_data,
)

router = APIRouter(prefix="/auth")


@router.get("/login")
async def yandex_login() -> RedirectResponse:
    return RedirectResponse(get_yandex_oauth_url())


@router.get("/callback", response_model=AuthTokens)
async def yandex_auth_callback(
    code: str, session: AsyncSession = SessionDep
) -> AuthTokens:

    try:
        token_data = await get_yandex_token_data(code)
    except HTTPStatusError:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Error during token obtaining"
        )

    yandex_access_token = token_data.get("access_token")

    yandex_user = await get_yandex_user(yandex_access_token)
    user = await get_or_create_user_by_yandex_user(session, yandex_user)

    return AuthTokens.model_validate(
        {
            "access_token": create_access_token(user.id),
            "refresh_token": create_refresh_token(user.id),
        }
    )


@router.get("/user/me", response_model=UserSchema)
async def user_me(
    session: AsyncSession = SessionDep, authorization: str = Header(...)
) -> UserSchema:
    current_user = await get_current_user(session, authorization)
    if current_user is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return current_user
