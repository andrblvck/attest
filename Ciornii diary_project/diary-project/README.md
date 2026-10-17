Ciornii Andrei

# diary — консольный дневник

Учебный проект (TI232, click, вариант 6 — **diary**). Консольная утилита для хранения заметок:
**Click** (команды) + **SQLAlchemy ORM** (работа с базой) + **SQLite** (файл `diary.db`).

## Возможности

| Команда | Что делает |
|---|---|
| `diary add "текст"` | добавляет новую заметку |
| `diary list` | выводит все заметки по порядку: id, дата создания, текст |
| `diary delete ID` | удаляет заметку по id; если заметки нет — понятная ошибка |

Дополнительно:

- бизнес-логика вынесена в `diary/logic.py` (функции принимают `Session` первым аргументом);
- ошибки обрабатываются: пустой текст, несуществующий id, неверный id, ошибки базы данных;
- все действия, предупреждения и ошибки пишутся в файл `app.log`;
- тесты `pytest` работают на SQLite в памяти (`sqlite:///:memory:`), файлы на диске не создаются.

## Структура проекта

```
diary/
  models.py       модель Note (SQLAlchemy)
  logic.py        add_note, list_notes, delete_note
  db.py           подключение к SQLite
  log_config.py   логирование в app.log
  cli.py          команды Click (add, list, delete)
tests/
  conftest.py     фикстуры pytest
  test_diary.py   тесты бизнес-логики
  test_cli.py     тесты команд
pyproject.toml    настройки проекта, pytest и Ruff
requirements.txt  зависимости
.gitignore
.pre-commit-config.yaml
```

## Установка

Нужен Python 3.10 или новее. Выполнять команды в папке проекта.

**Windows (PowerShell):**

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

**macOS / Linux:**

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

## Запуск

```
diary add "Моя первая заметка"
diary list
diary delete 1
diary --help
```

Если команда `diary` не находится, можно запускать так: `python -m diary list`.

Пример вывода `diary list`:

```
1	2026-10-17 12:30:05	Моя первая заметка
2	2026-10-17 12:31:10	Купить хлеб
```

Пример ошибки: `diary delete 99` выведет `Error: Заметка с id=99 не найдена` (код возврата 1).

## Тесты и проверка кода

```
pytest
ruff check .
ruff format --check .
```

Автоисправление стиля: `ruff check . --fix` и `ruff format .`

## Настройки (необязательно)

- `DIARY_DB_URL` — адрес базы (по умолчанию `sqlite:///diary.db`);
- `DIARY_LOG_FILE` — путь к файлу логов (по умолчанию `app.log`).
