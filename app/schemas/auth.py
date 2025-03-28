from fastapi.security import OAuth2AuthorizationCodeBearer
from pydantic import BaseModel, EmailStr

from app import config


class AuthTokens(BaseModel):
    access_token: str


class YandexDefaultPhone(BaseModel):
    id: int
    number: str


class YandexUserInfo(BaseModel):
    id: str
    login: str
    client_id: str
    display_name: str
    real_name: str
    first_name: str
    last_name: str
    sex: str
    default_email: EmailStr
    emails: list[EmailStr]
    birthday: str
    default_avatar_id: str
    is_avatar_empty: bool
    default_phone: YandexDefaultPhone | None
    psuid: str


oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=config.YANDEX_AUTH_URL, tokenUrl=config.YANDEX_TOKEN_URL
)
