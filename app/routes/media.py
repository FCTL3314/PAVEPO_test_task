from http import HTTPStatus

from fastapi import APIRouter, Form, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from app.dependencies import SessionDep
from app.repository.media import create_audio_media, get_medias_by_owner
from app.schemas.media import MediaSchema
from app.services.media import save_media_file

router = APIRouter(prefix="/media")


@router.post("/upload-audio")
async def upload_audio(
    user_id: int = Form(...),
    file: UploadFile = File(...),
    session: AsyncSession = SessionDep,
):
    if not file.content_type.startswith("audio/"):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Invalid file type. Audiofile required.",
        )

    file_location = await save_media_file(file.filename, file.file)

    new_media = await create_audio_media(
        session,
        file.filename,
        file_location,
        user_id,
    )

    return JSONResponse(
        status_code=HTTPStatus.CREATED,
        content={"message": "File was successfully uploaded", "media_id": new_media.id},
    )


@router.get("/user/{user_id}/audios", response_model=list[MediaSchema])
async def get_user_audios(user_id: int, session: AsyncSession = SessionDep):
    return await get_medias_by_owner(session, user_id)
