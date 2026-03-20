from fastapi import APIRouter

from app.api.endpoints import url_router

router = APIRouter(prefix='/url')

router.include_router(
    url_router
)
