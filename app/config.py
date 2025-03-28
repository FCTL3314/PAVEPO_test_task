from decouple import config as env_config
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    DEBUG: bool = env_config('DEBUG', cast=bool, default=False)

    DATABASE_NAME: str = env_config('DATABASE_NAME', cast=str)
    DATABASE_HOST: str = env_config('DATABASE_HOST', cast=str)
    DATABASE_PORT: int = env_config('DATABASE_PORT', cast=int)
    DATABASE_USER: str = env_config('DATABASE_USER', cast=str)
    DATABASE_PASSWORD: str = env_config('DATABASE_PASSWORD', cast=str)
