"""Бизнес-логика дневника.

Все функции принимают готовую Session первым аргументом и ничего не знают про Click.
"""

import logging

from sqlalchemy import select
from sqlalchemy.orm import Session

from diary.models import Note

log = logging.getLogger(__name__)


def add_note(session: Session, text: str) -> int:
    """Добавить заметку и вернуть её id. Пустой текст запрещён."""
    text = text.strip()
    if not text:
        log.warning('Попытка добавить пустую заметку')
        raise ValueError('Текст заметки не может быть пустым')
    note = Note(text=text)
    session.add(note)
    session.commit()
    log.info('Добавлена заметка id=%s', note.id)
    return note.id


def list_notes(session: Session) -> list[Note]:
    """Вернуть все заметки по порядку (по возрастанию id)."""
    notes = list(session.scalars(select(Note).order_by(Note.id)))
    log.info('Получен список заметок: %d шт.', len(notes))
    return notes


def delete_note(session: Session, note_id: int) -> bool:
    """Удалить заметку по id. Вернуть True, если удалена, и False, если такой заметки нет."""
    note = session.get(Note, note_id)
    if note is None:
        log.warning('Заметка id=%s не найдена, удалять нечего', note_id)
        return False
    session.delete(note)
    session.commit()
    log.info('Удалена заметка id=%s', note_id)
    return True


def format_note(note: Note) -> str:
    """Строка для вывода: id, дата создания, текст."""
    return f'{note.id}\t{note.created_at:%Y-%m-%d %H:%M:%S}\t{note.text}'
