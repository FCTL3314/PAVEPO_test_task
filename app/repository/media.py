from typing import Sequence, Any

from sqlalchemy import Select, RowMapping, Row
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.media import Media


async def create_audio_media(
    session: AsyncSession, filename: str, filepath: str, owner_id: str | int
) -> Media:
    new_media = Media(
        filename=filename,
        filepath=filepath,
        media_type="audio",
        owner_id=int(owner_id),
    )
    session.add(new_media)
    await session.commit()
    await session.refresh(new_media)
    return new_media


async def get_medias_by_owner(
    session: AsyncSession, owner_id: str | int
) -> Sequence[Row | RowMapping | Any]:
    result = await session.execute(
        Select(Media).filter(Media.owner_id == int(owner_id))
    )
    return result.scalars().all()
