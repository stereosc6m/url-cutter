from typing import Optional, List

from pydantic import BaseModel, Field

from .user import UserInfo
from .urls import UrlInfo


class CollectionCreate(BaseModel):
    title: str = Field(max_length=100)


class CollectionInfo(BaseModel):
    title: str
    user: UserInfo
    urls: List[UrlInfo]

    class Config:
        from_attributes = True
