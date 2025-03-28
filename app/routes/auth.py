from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from httpx import AsyncClient
from starlette.responses import RedirectResponse

from app import config
from app.dependencies.auth import Oauth2SchemeDep
from app.schemas.auth import AuthTokens, YandexUserInfo
from app.services.yandex import get_yandex_oauth_url, get_yandex_user_info

router = APIRouter(prefix="/auth")


@router.get("/login")
async def yandex_login() -> RedirectResponse:
    return RedirectResponse(get_yandex_oauth_url())


@router.get("/callback", response_model=AuthTokens)
async def yandex_auth_callback(code: str) -> AuthTokens:
    async with AsyncClient() as client:
        response = await client.post(
            config.YANDEX_TOKEN_URL,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "client_id": config.YANDEX_CLIENT_ID,
                "client_secret": config.YANDEX_CLIENT_SECRET,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
    if response.status_code != HTTPStatus.OK:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Error during token obtaining"
        )

    token_data = response.json()
    access_token = token_data.get("access_token")

    return AuthTokens.model_validate({"access_token": access_token})


@router.get("/user/me", response_model=YandexUserInfo)
async def yandex_user_info(token: str = Oauth2SchemeDep) -> YandexUserInfo:
    return await get_yandex_user_info(token)
