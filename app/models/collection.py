from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base, CommonMixin


class Collection(CommonMixin, Base):
    title: Mapped[str] = mapped_column(
        String(100),
        unique=False,
        nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('user.id'),
        nullable=False
    )

    user = relationship('User', back_populates='collections')
