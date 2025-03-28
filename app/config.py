from decouple import config as env_config
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    DEBUG: bool = env_config("DEBUG", cast=bool, default=False)

    DATABASE_NAME: str = env_config("DATABASE_NAME", cast=str)
    DATABASE_HOST: str = env_config("DATABASE_HOST", cast=str)
    DATABASE_PORT: int = env_config("DATABASE_PORT", cast=int)
    DATABASE_USER: str = env_config("DATABASE_USER", cast=str)
    DATABASE_PASSWORD: str = env_config("DATABASE_PASSWORD", cast=str)

    YANDEX_CLIENT_ID: str = env_config("YANDEX_CLIENT_ID", cast=str)
    YANDEX_CLIENT_SECRET: str = env_config("YANDEX_CLIENT_SECRET", cast=str)
    YANDEX_AUTH_URL: str = env_config(
        "YANDEX_AUTH_URL",
        default="https://oauth.yandex.ru/authorize",
        cast=str,
    )
    YANDEX_TOKEN_URL: str = env_config(
        "YANDEX_TOKEN_URL",
        default="https://oauth.yandex.ru/token",
        cast=str,
    )
    YANDEX_REDIRECT_URI: str = env_config(
        "YANDEX_REDIRECT_URI",
        default="http://localhost:8000/auth/callback",
        cast=str,
    )
