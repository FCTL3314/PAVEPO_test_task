from fastapi import Depends

from app.db import get_async_session

SessionDep = Depends(get_async_session)
