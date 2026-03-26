from typing import Optional

from pydantic import BaseModel, Field

from .user import UserInfo


class UrlCreate(BaseModel):
    original_url: str = Field(
        max_length=200,
        description='Ссылка',
    )
    short_url: Optional[str] = Field(
        max_length=16,
        description='Короткая ссылка',
        default=None
    )


class UrlInfo(UrlCreate):
    id: int
    user: UserInfo

    class Config:
        from_attributes = True
