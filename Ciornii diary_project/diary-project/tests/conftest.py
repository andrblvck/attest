"""Общие фикстуры pytest."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from diary.models import Base


@pytest.fixture
def session():
    """Чистая база SQLite в оперативной памяти для каждого теста."""
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    engine.dispose()


@pytest.fixture
def cli_env(tmp_path, monkeypatch):
    """Для тестов CLI: база и лог-файл во временной папке, а не в проекте."""
    db_file = tmp_path / 'test.db'
    log_file = tmp_path / 'app.log'
    monkeypatch.setenv('DIARY_DB_URL', f'sqlite:///{db_file.as_posix()}')
    monkeypatch.setenv('DIARY_LOG_FILE', str(log_file))
    return log_file
