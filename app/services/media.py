import os
import shutil
import uuid
from typing import BinaryIO

from app.constants import MEDIA_DIR


async def create_media_dir() -> None:
    os.makedirs(MEDIA_DIR, exist_ok=True)


async def save_media_file(filename: str, file: BinaryIO) -> str:
    file_extension = os.path.splitext(filename)[1]
    unique_filename = f"{uuid.uuid4().hex}{file_extension}"
    file_location = os.path.join(MEDIA_DIR, unique_filename)

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file, buffer)

    return file_location
