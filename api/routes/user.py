from fastapi import Depends, APIRouter, status

import app.models as m
import app.schema as s
from app.logger import log

from api.dependency import get_current_user


user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.get("/me", status_code=status.HTTP_200_OK, response_model=s.User)
def get_current_user_profile(
    current_user: m.User = Depends(get_current_user),
):
    """Returns the current user profile"""

    log(log.INFO, f"User {current_user.username} requested his profile")
    return current_user
