import uuid

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import UserNotFound
from app.models.auth import User
from app.schemas.auth import UpdateUser as UpdateUserSchema
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


async def get_user_by_id(session: AsyncSession, _id: int | str) -> User:
    result = await session.execute(select(User).filter(User.id == int(_id)))
    user = result.scalars().first()
    if user is None:
        raise UserNotFound
    return user


async def update_user(session: AsyncSession, current_user: User, updated_user: UpdateUserSchema) -> User:
    try:
        user = await get_user_by_id(session, current_user.id)

        for field, value in updated_user.model_dump().items():
            if value is None:
                continue
            setattr(user, field, value)

        await session.commit()
        await session.refresh(user)

        return user
    except NoResultFound:
        raise UserNotFound
