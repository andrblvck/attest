"""Подключение к базе данных SQLite."""

import os
from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from diary.models import Base

DEFAULT_DB_URL = 'sqlite:///diary.db'


def get_db_url() -> str:
    """Адрес базы: из переменной окружения DIARY_DB_URL или файл diary.db в текущей папке."""
    return os.environ.get('DIARY_DB_URL', DEFAULT_DB_URL)


@contextmanager
def get_session() -> Iterator[Session]:
    """Создать таблицы (если их нет) и выдать сессию."""
    engine = create_engine(get_db_url())
    Base.metadata.create_all(engine)
    try:
        with Session(engine) as session:
            yield session
    finally:
        engine.dispose()
