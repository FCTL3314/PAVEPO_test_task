from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Header
from httpx import HTTPStatusError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse

from app.dependencies import SessionDep
from app.exceptions import UserNotFound
from app.repository.auth import (
    get_or_create_user_by_yandex_user,
    get_user_by_id,
    update_user,
)
from app.schemas.auth import (
    AuthTokens,
    RefreshTokensInput,
    UpdateUser,
    User,
    OutputUser,
)
from app.services.auth import (
    get_current_user,
    decode_refresh_token,
    create_auth_tokens_for_user_id,
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

    return create_auth_tokens_for_user_id(user.id)


@router.get("/user/me", response_model=User)
async def get_user_me(
    session: AsyncSession = SessionDep, authorization: str = Header(...)
) -> User:
    try:
        current_user = await get_current_user(session, authorization)
    except UserNotFound:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return current_user


@router.patch("/user/me", response_model=OutputUser)
async def update_user_me(
    updated_user: UpdateUser,
    session: AsyncSession = SessionDep,
    authorization: str = Header(...),
) -> User:
    try:
        current_user = await get_current_user(session, authorization)
    except UserNotFound:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    updated_user = await update_user(session, current_user, updated_user)
    return updated_user


@router.post("/token/refresh", response_model=AuthTokens)
async def refresh_access_token(
    refresh_tokens_input: RefreshTokensInput, session: AsyncSession = SessionDep
) -> AuthTokens:
    try:
        payload = decode_refresh_token(refresh_tokens_input.refresh_token)
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail=str(e))

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Token payload invalid: missing subject",
        )

    try:
        user = await get_user_by_id(session, user_id)
    except UserNotFound:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")

    return create_auth_tokens_for_user_id(user.id)
