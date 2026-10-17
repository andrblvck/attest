"""Настройка логирования в файл app.log."""

import logging
import os

LOG_FORMAT = '%(asctime)s %(levelname)s %(name)s: %(message)s'

_file_handler: logging.Handler | None = None


def setup_logging() -> None:
    """Писать логи в app.log (путь можно изменить переменной DIARY_LOG_FILE)."""
    global _file_handler
    log_file = os.environ.get('DIARY_LOG_FILE', 'app.log')
    logger = logging.getLogger('diary')
    logger.setLevel(logging.INFO)
    if _file_handler is not None:
        logger.removeHandler(_file_handler)
        _file_handler.close()
    _file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
    _file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(_file_handler)
