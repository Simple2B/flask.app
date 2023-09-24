from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.api.oauth2 import verify_access_token, INVALID_CREDENTIALS_EXCEPTION
from app.database import get_db
import app.models as m
import app.schema as s
from app.logger import log

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> m.User:
    """Raises an exception if the current user is not authenticated"""
    # TODO: refactor this function
    return None
    token: s.TokenData = verify_access_token(token, INVALID_CREDENTIALS_EXCEPTION)
    user = db.query(m.User).filter_by(id=token.user_id).first()
    if not user:
        log(log.INFO, "User wasn`t authtorized")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User wasn`t authtorized",
        )
    if user.is_deleted:
        log(log.INFO, "User wasn't found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User wasn't found",
        )
    return user


def get_user(request: Request, db: Session = Depends(get_db)) -> m.User | None:
    """Raises an exception if the current user is authenticated"""
    auth_header: str = request.headers.get("Authorization")
    if auth_header:
        # Assuming the header value is in the format "Bearer <token>"
        token: s.TokenData = verify_access_token(
            auth_header.split(" ")[1], INVALID_CREDENTIALS_EXCEPTION
        )
        user = db.scalar(
            select(m.User).where(
                m.User.id == token.user_id,
                m.User.is_deleted.is_(False),
            )
        )
        return user
    return None
