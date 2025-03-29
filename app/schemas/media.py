from pydantic import BaseModel


class MediaSchema(BaseModel):
    id: int
    filename: str
    filepath: str
    media_type: str

    class Config:
        orm_mode = True
