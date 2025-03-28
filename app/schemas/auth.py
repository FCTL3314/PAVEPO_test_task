from datetime import datetime

from fastapi.security import OAuth2AuthorizationCodeBearer
from pydantic import BaseModel, EmailStr

from app import settings


class AuthTokens(BaseModel):
    access_token: str
    refresh_token: str


class YandexDefaultPhone(BaseModel):
    id: int
    number: str


class YandexUser(BaseModel):
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
    authorizationUrl=settings.YANDEX_AUTH_URL, tokenUrl=settings.YANDEX_TOKEN_URL
)


class User(BaseModel):
    id: int
    yandex_id: str
    username: str
    email: str
    password_hash: str
    created_at: datetime

    class Config:
        orm_mode = True
