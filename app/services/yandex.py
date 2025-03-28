from httpx import AsyncClient

from app import settings
from app.schemas.auth import YandexUserInfo


def get_yandex_oauth_url() -> str:
    return (
        f"{settings.YANDEX_AUTH_URL}"
        f"?response_type=code"
        f"&client_id={settings.YANDEX_CLIENT_ID}"
        f"&redirect_uri={settings.YANDEX_REDIRECT_URI}"
    )


async def get_yandex_user_info(access_token: str) -> YandexUserInfo:
    async with AsyncClient() as client:
        response = await client.get(
            "https://login.yandex.ru/info",
            headers={"Authorization": f"OAuth {access_token}"},
        )
    return YandexUserInfo.model_validate(response.json())
