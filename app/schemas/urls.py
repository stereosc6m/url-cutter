from typing import Optional

from pydantic import BaseModel, HttpUrl, Field

from .user import UserInfo


class UrlCreate(BaseModel):
    original_url: HttpUrl
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
