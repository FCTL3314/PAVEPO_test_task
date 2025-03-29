from app.services.media import create_media_dir


async def on_startup() -> None:
    await create_media_dir()
