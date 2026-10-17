"""Тесты бизнес-логики (diary.logic) на sqlite в памяти."""

import pytest

from diary.logic import add_note, delete_note, format_note, list_notes


def test_add_note_returns_id(session):
    note_id = add_note(session, 'первая заметка')
    assert note_id == 1


def test_add_note_ids_increase(session):
    first = add_note(session, 'a')
    second = add_note(session, 'b')
    assert second == first + 1


def test_add_note_strips_text(session):
    add_note(session, '  привет  ')
    assert list_notes(session)[0].text == 'привет'


@pytest.mark.parametrize('text', ['', '   ', '\n\t'])
def test_add_note_rejects_empty_text(session, text):
    with pytest.raises(ValueError, match='не может быть пустым'):
        add_note(session, text)
    assert list_notes(session) == []


def test_list_notes_empty(session):
    assert list_notes(session) == []


def test_list_notes_in_order(session):
    add_note(session, 'one')
    add_note(session, 'two')
    add_note(session, 'three')
    assert [note.text for note in list_notes(session)] == ['one', 'two', 'three']


def test_note_has_creation_date(session):
    add_note(session, 'с датой')
    assert list_notes(session)[0].created_at is not None


def test_delete_note_removes_existing_note(session):
    note_id = add_note(session, 'удалить меня')
    assert delete_note(session, note_id) is True
    assert list_notes(session) == []


def test_delete_note_keeps_other_notes(session):
    keep = add_note(session, 'оставить')
    remove = add_note(session, 'удалить')
    delete_note(session, remove)
    assert [note.id for note in list_notes(session)] == [keep]


def test_delete_note_missing_returns_false(session):
    assert delete_note(session, 999) is False


def test_format_note_contains_id_date_and_text(session):
    add_note(session, 'текст заметки')
    note = list_notes(session)[0]
    line = format_note(note)
    assert line.startswith('1\t')
    assert f'{note.created_at:%Y-%m-%d}' in line
    assert line.endswith('текст заметки')
