from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.urls import urls_crud
from app.schemas.urls import UrlCreate, UrlInfo
from app.api.validators import (
    is_object_exist,
    is_short_url_exist
)
from app.models.user import User


async def creating_url(
    obj_in: UrlCreate,
    session: AsyncSession,
    user: User
) -> UrlInfo:
    result = await urls_crud.get_by_original_url(
        obj_in.original_url,
        session
    )
    if result is not None and obj_in.short_url is None:
        return result
    if obj_in.short_url is not None:
        result = await urls_crud.get_by_short_url(
            obj_in.short_url,
            session
        )
        is_short_url_exist(result)
    return await urls_crud.safe_new_url(obj_in, session, user)


async def get_one_url_by_short_link(
    short_url: int,
    session: AsyncSession
) -> UrlInfo:
    result = await urls_crud.get_by_short_url(short_url, session)
    is_object_exist(result)
    return result


async def get_all_urls(
    session: AsyncSession
) -> List[UrlInfo]:
    return await urls_crud.get_urls_list(session)


async def get_sequency_of_user_urls(
    user: User,
    session: AsyncSession
) -> List[UrlInfo]:
    return await urls_crud.get_user_urls(user, session)
