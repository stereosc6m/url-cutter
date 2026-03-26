from fastapi import FastAPI

from app.api.routers import router
from app.api.endpoints import user_router
from app.core.config import settings

app = FastAPI(title=settings.app_title)

app.include_router(router)
app.include_router(user_router)