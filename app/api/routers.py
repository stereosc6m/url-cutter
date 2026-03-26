from fastapi import APIRouter

from app.api.endpoints import url_router, collection_router

router = APIRouter()

router.include_router(
    url_router,
    prefix='/url'
)

router.include_router(
    collection_router,
    prefix='/collection'
)
