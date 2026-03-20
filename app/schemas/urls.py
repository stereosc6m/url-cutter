from typing import Optional

from pydantic import BaseModel, Field


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
