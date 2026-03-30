from random import choice, randint
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.schemas.urls import UrlCreate, UrlInfo
from app.models import UrlModel, User, UrlCollection
from app.core.constants import URL_GENERATOR


class UrlCRUD():

    def __init__(
            self,
            model: UrlModel
    ):
        self.model = model

    async def safe_new_url(
        self,
        obj_in: UrlCreate,
        session: AsyncSession,
        user: User
    ) -> UrlInfo:
        object_in = obj_in.model_dump()
        object_in['user_id'] = user.id
        if object_in['short_url'] is None:
            short_link = ''
            for _ in range(randint(1, 16)):
                short_link += choice(URL_GENERATOR)
            object_in['short_url'] = short_link
        object_db = self.model(**object_in)
        session.add(object_db)
        await session.commit()
        return object_db

    async def get_by_original_url(
        self,
        original_url: str,
        session: AsyncSession
    ) -> UrlModel:
        result = await session.execute(
            select(self.model).where(
                self.model.original_url == original_url
            )
        )
        return result.scalars().one_or_none()

    async def get_by_short_url(
        self,
        short_url: str,
        session: AsyncSession
    ) -> UrlModel:
        result = await session.execute(
            select(self.model).options(
                joinedload(self.model.user)
            ).where(
                self.model.short_url == short_url
            )
        )
        return result.scalars().one_or_none()

    async def get_by_url_id(
        self,
        url_id: int,
        session: AsyncSession
    ) -> UrlModel:
        result = await session.execute(
            select(self.model).options(
                joinedload(self.model.user)
            ).where(
                self.model.id == url_id
            )
        )
        return result.scalars().one_or_none()

    async def get_user_urls(
        self,
        user: User,
        session: AsyncSession
    ) -> List[UrlModel]:
        result = await session.execute(
            select(self.model).options(
                joinedload(self.model.user)
            ).where(
                self.model.user_id == user.id
            )
        )
        return result.scalars().all()

    async def save_url_to_collection(
        self,
        url_id: int,
        collection_id: int,
        session: AsyncSession
    ) -> None:
        obj_db = UrlCollection(url_id=url_id, collection_id=collection_id)
        session.add(obj_db)
        await session.commit()
        return None


urls_crud = UrlCRUD(UrlModel)
