
from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user
from app.models.user import User
from app.schemas.collection import CollectionCreate, CollectionInfo
from app.services.collection import create_new_collection


SessionDep = Annotated[AsyncSession, Depends(get_async_session)]

router = APIRouter()


@router.post('/')
async def create_user_collection(
    obj_in: CollectionCreate,
    session: SessionDep,
    user: Annotated[User, Depends(current_user)]
) -> CollectionInfo:
    return await create_new_collection(
        obj_in,
        user,
        session
    )
