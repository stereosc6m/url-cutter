from typing import Optional

from pydantic import BaseModel, Field

from .user import UserInfo


class CollectionCreate(BaseModel):
    title: str = Field(max_length=100)


class CollectionInfo(BaseModel):
    title: str
    user: UserInfo

    class Config:
        from_attributes = True
