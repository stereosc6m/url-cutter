
from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user
from app.models.user import User
from app.schemas.collection import CollectionCreate, CollectionInfo
from app.services.collection import (
    create_new_collection,
    get_collection,
    get_collections
)


SessionDep = Annotated[AsyncSession, Depends(get_async_session)]

router = APIRouter(tags=['Коллекции'])


@router.post(
    '/',
    summary='Создать коллекцию',
    description='Возвращает объект созданной коллекции'
    )
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


@router.get(
    '/{collection_id}',
    summary='Получить объект коллекции',
    description='Возвращает коллекцию и связанные с ней объекты'
    )
async def view_collection(
    collection_id: int,
    user: Annotated[User, Depends(current_user)],
    session: SessionDep
) -> CollectionInfo:
    return await get_collection(
        collection_id,
        user,
        session
    )


@router.get(
    '/',
    summary='Получить список коллекций пользователя',
    description='Возвращает список коллекций пользователя'
    )
async def view_user_collections(
    user: Annotated[User, Depends(current_user)],
    session: SessionDep
) -> List[CollectionInfo]:
    return await get_collections(user, session)
