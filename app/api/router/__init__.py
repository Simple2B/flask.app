# flake8: noqa F401
from fastapi import APIRouter, Request

from .user import user_router

# from .notify import notification_test_router


router = APIRouter(prefix="/api", tags=["API"])

router.include_router(user_router)


@router.get("/list-endpoints/")
def list_endpoints(request: Request):
    url_list = [
        {"path": route.path, "name": route.name} for route in request.app.routes
    ]
    return url_list
