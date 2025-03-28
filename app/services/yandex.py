from http import HTTPStatus
from typing import Any

from fastapi import HTTPException
from httpx import AsyncClient

from app import settings
from app.schemas.auth import YandexUser


def get_yandex_oauth_url() -> str:
    return (
        f"{settings.YANDEX_AUTH_URL}"
        f"?response_type=code"
        f"&client_id={settings.YANDEX_CLIENT_ID}"
        f"&redirect_uri={settings.YANDEX_REDIRECT_URI}"
    )


async def get_yandex_user(access_token: str) -> YandexUser:
    async with AsyncClient() as client:
        response = await client.get(
            "https://login.yandex.ru/info",
            headers={"Authorization": f"OAuth {access_token}"},
        )
    return YandexUser.model_validate(response.json())


async def get_yandex_token_data(code: str) -> dict[str, Any]:
    async with AsyncClient() as client:
        response = await client.post(
            settings.YANDEX_TOKEN_URL,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "client_id": settings.YANDEX_CLIENT_ID,
                "client_secret": settings.YANDEX_CLIENT_SECRET,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        response.raise_for_status()

    return response.json()
