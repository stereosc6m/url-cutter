from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.collection import collection_crud
from app.schemas.collection import CollectionCreate, CollectionInfo
from app.models.user import User


async def create_new_collection(
    obj_in: CollectionCreate,
    user: User,
    session: AsyncSession
) -> CollectionInfo:
    return await collection_crud.save_new_collection(
        obj_in,
        user,
        session
    )
