from sqlalchemy import Column, String, Integer, DateTime, func, Boolean

from app.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    yandex_id = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, nullable=False, unique=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    password_hash = Column(String, nullable=True)
    is_superuser = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=func.now())
