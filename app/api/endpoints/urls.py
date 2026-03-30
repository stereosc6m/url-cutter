from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.urls import (
    creating_url,
    get_one_url_by_short_link,
    get_sequency_of_user_urls,
    add_url_and_collection
)
from app.schemas.urls import UrlCreate, UrlInfo
from app.core.db import get_async_session
from app.core.user import current_user
from app.models import User

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]

router = APIRouter(tags=['URL'])


@router.post('/')
async def url_create(
    url_in: UrlCreate,
    session: SessionDep,
    user: Annotated[User, Depends(current_user)]
) -> UrlInfo:
    return await creating_url(url_in, session, user)


@router.get('/{url_short_link}')
async def url_get_by_short_link(
    url_short_link: str,
    session: SessionDep
) -> UrlInfo:
    return await get_one_url_by_short_link(url_short_link, session)


@router.post('/{url_id}/{collection_id}')
async def add_url_to_collection(
    url_id: int,
    collection_id: int,
    session: SessionDep
) -> UrlInfo:
    return await add_url_and_collection(
        url_id, collection_id, session
    )

@router.get('/')
async def urls_user_get(
    user: Annotated[User, Depends(current_user)],
    session: SessionDep
) -> List[UrlInfo]:
    return await get_sequency_of_user_urls(user, session)
