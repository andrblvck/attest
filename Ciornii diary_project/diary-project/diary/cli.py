"""Командный интерфейс (Click). Только разбор команд и вывод, логика — в diary.logic."""

import logging

import click
from sqlalchemy.exc import SQLAlchemyError

from diary.db import get_session
from diary.log_config import setup_logging
from diary.logic import add_note, delete_note, format_note, list_notes

log = logging.getLogger(__name__)

DB_ERROR_MESSAGE = 'Ошибка базы данных. Подробности в app.log'


@click.group()
def cli() -> None:
    """Дневник: добавляйте, просматривайте и удаляйте заметки."""
    setup_logging()


@cli.command()
@click.argument('text')
def add(text: str) -> None:
    """Добавить новую заметку."""
    try:
        with get_session() as session:
            note_id = add_note(session, text)
    except ValueError as error:
        raise click.ClickException(str(error)) from error
    except SQLAlchemyError as error:
        log.exception('Ошибка базы данных при добавлении заметки')
        raise click.ClickException(DB_ERROR_MESSAGE) from error
    click.echo(f'Заметка добавлена (id={note_id})')


@cli.command(name='list')
def list_command() -> None:
    """Вывести все заметки: id, дата создания, текст."""
    try:
        with get_session() as session:
            lines = [format_note(note) for note in list_notes(session)]
    except SQLAlchemyError as error:
        log.exception('Ошибка базы данных при чтении заметок')
        raise click.ClickException(DB_ERROR_MESSAGE) from error
    if not lines:
        click.echo('Заметок пока нет')
        return
    for line in lines:
        click.echo(line)


@cli.command()
@click.argument('note_id', type=int)
def delete(note_id: int) -> None:
    """Удалить заметку по id."""
    try:
        with get_session() as session:
            deleted = delete_note(session, note_id)
    except SQLAlchemyError as error:
        log.exception('Ошибка базы данных при удалении заметки')
        raise click.ClickException(DB_ERROR_MESSAGE) from error
    if not deleted:
        raise click.ClickException(f'Заметка с id={note_id} не найдена')
    click.echo(f'Заметка id={note_id} удалена')


if __name__ == '__main__':
    cli()
