from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.urls import (
    creating_url,
    get_one_url_by_id,
    get_one_url_by_short_link,
    get_all_urls
)
from app.schemas.urls import UrlCreate, UrlInfo
from app.core.db import get_async_session

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]

router = APIRouter()


@router.post('/')
async def url_create(
    url_in: UrlCreate,
    session: SessionDep
) -> UrlInfo:
    return await creating_url(url_in, session)


@router.get('/{url_id}')
async def url_get_by_id(
    url_id: int,
    session: SessionDep
) -> UrlInfo:
    return await get_one_url_by_id(url_id, session)


@router.get('/{url_short_link}')
async def url_get_by_short_link(
    url_short_link: str,
    session: SessionDep
) -> UrlInfo:
    return await get_one_url_by_short_link(url_short_link, session)


@router.get('/')
async def urls_get(
    session: SessionDep
) -> List[UrlInfo]:
    return await get_all_urls(session)
