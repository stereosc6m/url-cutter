from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.user import User
from app.models.collection import Collection
from app.models.urls import UrlModel, UrlCollection
from app.schemas.collection import CollectionCreate


class CollectionCRUD():

    def __init__(
        self,
        model: Collection
    ):
        self.model = model

    async def save_new_collection(
        self,
        obj_in: CollectionCreate,
        user: User,
        session: AsyncSession
    ) -> Collection:
        obj_in = obj_in.model_dump()
        obj_in['user_id'] = user.id
        result = Collection(**obj_in)
        session.add(result)
        await session.commit()
        return result

    async def get_linked_urls_id(
        self,
        collection_id: int,
        session: AsyncSession
    ) -> List:
        urls_result = await session.execute(
            select(UrlCollection.url_id).where(
                UrlCollection.collection_id == collection_id
            )
        )
        return urls_result.scalars().all()

    async def get_linked_urls(
        self,
        urls_id: List[int],
        session: AsyncSession
    ) -> List[UrlModel]:
        result = await session.execute(
            select(UrlModel)
            .where(UrlModel.id.in_(urls_id))
            .options(
                joinedload(UrlModel.user)
            )
        )
        return result.scalars().all()

    async def get_collection_by_id(
        self,
        collection_id: int,
        session: AsyncSession
    ) -> Collection:
        result = await session.execute(
            select(self.model).where(
                self.model.id == collection_id
            ).options(joinedload(Collection.user))
        )
        return result.scalars().one_or_none()

    async def get_collections_from_db(
        self,
        user: User,
        session: AsyncSession
    ) -> List[Collection]:
        result = await session.execute(
            select(self.model).where(
                self.model.user_id == user.id
            ).options(joinedload(Collection.user))
        )
        return result.scalars().all()


collection_crud = CollectionCRUD(Collection)
