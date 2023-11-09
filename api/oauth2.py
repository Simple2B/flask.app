from datetime import datetime, timedelta
from fastapi import status
from jose import JWTError, jwt
from fastapi import HTTPException
from pydantic import ValidationError

import app.schema as s
from config import config

CFG = config()

SECRET_KEY = CFG.JWT_SECRET
ACCESS_TOKEN_EXPIRE_MINUTES = CFG.ACCESS_TOKEN_EXPIRE_MINUTES

INVALID_CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def create_access_token(user_id: int) -> str:
    to_encode = s.TokenData(
        user_id=user_id,
        exp=datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    ).model_dump()

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception) -> s.TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY)
        token_data = s.TokenData.model_validate(payload)
    except ValidationError:
        raise credentials_exception
    except JWTError:
        raise credentials_exception

    return token_data
