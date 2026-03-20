from random import choice, randint
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.urls import UrlCreate, UrlInfo
from app.models.urls import UrlModel
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
        session: AsyncSession
    ) -> UrlInfo:
        object_in = obj_in.model_dump()
        if object_in['short_url'] is None:
            short_link = ''
            for _ in range(randint(1, 17)):
                short_link += choice(URL_GENERATOR)
            object_in['short_url'] = short_link
        object_db = self.model(**object_in)
        session.add(object_db)
        await session.commit()
        return object_db

    async def get_url_by_id(
        self,
        url_id: int,
        session: AsyncSession
    ) -> UrlModel:
        result = await session.execute(
            select(self.model).where(
                self.model.id == url_id
            )
        )
        return result.scalars().one_or_none()

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
            select(self.model).where(
                self.model.short_url == short_url
            )
        )
        return result.scalars().one_or_none()

    async def get_urls_list(
        self,
        session: AsyncSession
    ) -> List[UrlModel]:
        result = await session.execute(
            select(self.model)
        )
        return result.scalars().all()


urls_crud = UrlCRUD(UrlModel)
