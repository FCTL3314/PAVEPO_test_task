from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Literal

import jwt
from fastapi import Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import settings
from app.constants import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    REFRESH_TOKEN_EXPIRE_DAYS,
)
from app.dependencies import SessionDep
from app.models.auth import User
from app.repository.auth import get_user_by_id


def create_jwt_token(
    user_id: int, lifetime: timedelta, token_type: Literal["access", "refresh"]
) -> str:
    expire = datetime.utcnow() + lifetime
    payload = {"sub": str(user_id), "exp": expire, "type": token_type}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)


def create_access_token(user_id: int) -> str:
    return create_jwt_token(
        user_id, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES), "access"
    )


def create_refresh_token(user_id: int) -> str:
    return create_jwt_token(
        user_id, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS), "refresh"
    )


def decode_token(token: str, token_type: Literal["access", "refresh"]) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != token_type:
            raise Exception("Invalid token type")
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")


def decode_access_token(token: str) -> dict:
    return decode_token(token, token_type="access")


def decode_refresh_token(token: str) -> dict:
    return decode_token(token, token_type="refresh")


async def get_current_user(
    session: AsyncSession, authorization: str = Header(...)
) -> User:
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid token format"
        )
    token = authorization.split(" ")[1]
    try:
        payload = decode_access_token(token)
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail=str(e))
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Token payload invalid: missing subject",
        )

    return await get_user_by_id(session, user_id)
