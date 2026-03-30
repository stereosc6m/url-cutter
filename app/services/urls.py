from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.urls import urls_crud
from app.crud.collection import collection_crud
from app.schemas.urls import UrlCreate, UrlInfo
from app.api.validators import (
    is_url_exist,
    is_short_url_exist,
    is_objects_exist_and_user_author_collection,
    is_relation_exist
)
from app.models.user import User


async def creating_url(
    obj_in: UrlCreate,
    session: AsyncSession,
    user: User
) -> UrlInfo:
    result = await urls_crud.get_by_original_url(
        str(obj_in.original_url),
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
    await urls_crud.safe_new_url(obj_in, session, user)
    return await urls_crud.get_by_original_url(
        str(obj_in.original_url),
        session
    )


async def get_one_url_by_short_link(
    short_url: int,
    session: AsyncSession
) -> UrlInfo:
    result = await urls_crud.get_by_short_url(short_url, session)
    is_url_exist(result)
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


async def add_url_and_collection(
    url_id: int,
    collection_id: int,
    user: User,
    session: AsyncSession
) -> UrlInfo:
    collection_db = await collection_crud.get_collection_by_id(
        collection_id, session
    )
    url_db = await urls_crud.get_by_url_id(
        url_id, session
    )
    is_objects_exist_and_user_author_collection(
        collection_db,
        url_db,
        user
    )
    url_and_collection = await urls_crud.get_relation_url_and_collection(
        url_id, collection_id, session
    )
    is_relation_exist(url_and_collection)
    await urls_crud.save_url_to_collection(
        url_id, collection_id, session
    )
    return await urls_crud.get_by_url_id(
        url_id, session
    )
