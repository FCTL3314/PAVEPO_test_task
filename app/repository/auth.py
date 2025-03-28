import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.auth import User
from app.schemas.auth import YandexUser


async def get_or_create_user_by_yandex_user(
    session: AsyncSession, yandex_user: YandexUser
) -> User:
    result = await session.execute(
        select(User).filter(User.yandex_id == yandex_user.id)
    )
    user = result.scalars().first()
    if not user:
        random_password = uuid.uuid4().hex

        user = User(
            yandex_id=yandex_user.id,
            username=yandex_user.login,
            email=str(yandex_user.default_email),
            password_hash=random_password,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
    return user


async def get_user_by_id(session: AsyncSession, _id: int | str) -> User | None:
    result = await session.execute(select(User).filter(User.id == int(_id)))
    return result.scalars().first()
