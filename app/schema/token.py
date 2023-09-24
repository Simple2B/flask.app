from pydantic import BaseModel
from config import config

CFG = config()


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: str = None
