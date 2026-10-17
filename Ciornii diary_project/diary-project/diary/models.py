"""Модель базы данных."""

from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Базовый класс для всех моделей."""


class Note(Base):
    """Заметка дневника."""

    __tablename__ = 'notes'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    def __repr__(self) -> str:
        return f'Note(id={self.id!r}, created_at={self.created_at!r}, text={self.text!r})'
