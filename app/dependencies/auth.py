from fastapi import Depends

from app.schemas.auth import oauth2_scheme

Oauth2SchemeDep = Depends(oauth2_scheme)
