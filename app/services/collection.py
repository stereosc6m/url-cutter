from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import is_collection_exist_and_available
from app.crud.collection import collection_crud
from app.schemas.collection import CollectionCreate, CollectionInfo
from app.models.user import User


async def create_new_collection(
    obj_in: CollectionCreate,
    user: User,
    session: AsyncSession
) -> CollectionInfo:
    collection_db = await collection_crud.save_new_collection(
        obj_in,
        user,
        session
    )
    collection_db = await collection_crud.get_collection_by_id(
        collection_db.id, session
    )
    collection_response = CollectionInfo(
        title=collection_db.title,
        user=collection_db.user,
        urls=[]
    )
    return collection_response


async def get_collection(
    collection_id: int,
    user: User,
    session: AsyncSession
) -> CollectionInfo:
    collection_db = await collection_crud.get_collection_by_id(
        collection_id, session
    )
    is_collection_exist_and_available(collection_db, user)
    urls_id = await collection_crud.get_linked_urls_id(
        collection_id, session
    )
    urls_db = await collection_crud.get_linked_urls(
        urls_id, session
    )
    collection_response = CollectionInfo(
        title=collection_db.title,
        user=collection_db.user,
        urls=urls_db
    )
    return collection_response


async def get_collections(
    user: User,
    session: AsyncSession
) -> List[CollectionInfo]:
    collections_db = await collection_crud.get_collections_from_db(
        user, session
    )
    collections = []
    for collection in collections_db:
        urls_id = await collection_crud.get_linked_urls_id(
            collection.id, session
        )
        urls_db = await collection_crud.get_linked_urls(
            urls_id, session
        )
        collection_response = CollectionInfo(
            title=collection.title,
            user=collection.user,
            urls=urls_db
        )
        collections.append(collection_response)
    return collections
