from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base, CommonMixin


class UrlModel(CommonMixin, Base):
    original_url: Mapped[str] = mapped_column(
        String(200),
        unique=False,
        nullable=False
    )
    short_url: Mapped[str] = mapped_column(
        String(16),
        unique=True,
        nullable=False
    )
