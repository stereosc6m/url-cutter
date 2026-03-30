from sqlalchemy import String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

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
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('user.id'),
        nullable=True
    )

    user = relationship('User', back_populates='urls')


class UrlCollection(CommonMixin, Base):
    url_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('urlmodel.id'),
        nullable=False
    )
    collection_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('collection.id'),
        nullable=False
    )

    url = relationship('UrlModel', back_populates='collections')
    collection = relationship('Collection', back_populates='urls')

    __table_args__ = (
        UniqueConstraint('url_id', 'collection_id', name='uq_url_collection'),
    )
