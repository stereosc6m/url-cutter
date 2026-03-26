from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.user import User
from app.models.collection import Collection
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


collection_crud = CollectionCRUD(Collection)
