from typing import Annotated
from fastapi import Depends, APIRouter, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from api.oauth2 import create_access_token

import app.models as m
from app import schema as s
from app.logger import log
from api.dependency import get_db


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", status_code=status.HTTP_200_OK, response_model=s.Token)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db=Depends(get_db)):
    """Logs in a user"""
    user = m.User.authenticate(form_data.username, form_data.password, session=db)
    if not user:
        log(log.ERROR, "User [%s] wrong username or password", form_data.username)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    log(log.INFO, "User [%s] logged in", user.username)
    return s.Token(access_token=create_access_token(user.id))


@router.post("/token", status_code=status.HTTP_200_OK, response_model=s.Token)
def get_token(auth_data: s.Auth, db=Depends(get_db)):
    """Logs in a user"""
    user = m.User.authenticate(auth_data.username, auth_data.password, session=db)
    if not user:
        log(log.ERROR, "User [%s] wrong username or password", auth_data.username)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    return s.Token(access_token=create_access_token(user.id))
