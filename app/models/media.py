from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db import Base


class Media(Base):
    __tablename__ = "media"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    filepath = Column(String, nullable=False)
    media_type = Column(String, default="audio")
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="audios")
