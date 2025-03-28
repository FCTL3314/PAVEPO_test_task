from fastapi import Depends

from app.schemas.auth import oauth2_scheme
from app.services.auth import get_current_user

Oauth2SchemeDep = Depends(oauth2_scheme)
CurrentUserDep = Depends(get_current_user)
