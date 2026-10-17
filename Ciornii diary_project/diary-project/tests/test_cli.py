"""Тесты командного интерфейса (Click) через CliRunner."""

from click.testing import CliRunner

from diary.cli import cli


def run(*args):
    return CliRunner().invoke(cli, list(args))


def test_add_command(cli_env):
    result = run('add', 'купить хлеб')
    assert result.exit_code == 0
    assert 'Заметка добавлена (id=1)' in result.output


def test_add_empty_text_shows_error(cli_env):
    result = run('add', '   ')
    assert result.exit_code != 0
    assert 'не может быть пустым' in result.output


def test_add_without_argument_shows_usage_error(cli_env):
    result = run('add')
    assert result.exit_code == 2
    assert 'Missing argument' in result.output


def test_list_empty(cli_env):
    result = run('list')
    assert result.exit_code == 0
    assert 'Заметок пока нет' in result.output


def test_list_shows_notes_in_order(cli_env):
    run('add', 'первая')
    run('add', 'вторая')
    result = run('list')
    assert result.exit_code == 0
    lines = result.output.strip().splitlines()
    assert lines[0].startswith('1\t')
    assert lines[0].endswith('первая')
    assert lines[1].startswith('2\t')
    assert lines[1].endswith('вторая')


def test_delete_existing_note(cli_env):
    run('add', 'временная')
    result = run('delete', '1')
    assert result.exit_code == 0
    assert 'удалена' in result.output
    assert 'Заметок пока нет' in run('list').output


def test_delete_missing_note_shows_clear_error(cli_env):
    result = run('delete', '42')
    assert result.exit_code == 1
    assert 'Заметка с id=42 не найдена' in result.output


def test_delete_non_integer_id_shows_error(cli_env):
    result = run('delete', 'abc')
    assert result.exit_code == 2


def test_actions_are_logged_to_file(cli_env):
    run('add', 'для лога')
    run('delete', '777')
    content = cli_env.read_text(encoding='utf-8')
    assert 'INFO' in content
    assert 'Добавлена заметка id=1' in content
    assert 'WARNING' in content
    assert 'id=777 не найдена' in content
