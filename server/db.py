from __future__ import annotations

import sqlite3
from pathlib import Path
from sqlite3 import Cursor, Connection
from typing import Optional, List

from server import settings

BASE_DIR: Path = Path(__file__).parent


def _init_db(database: Path = settings.DATABASE,
             create_db_script: Path = settings.DATABASE_INIT_SCRIPT,
             **kwargs):
    """
    Проверяем существование БД и создаём новую в случае отсутствия.
    :param database: файл базы данных
    :param create_db_script: sql скрипт создания таблиц баз данных
    :param kwargs: кварги
    """
    if not database.exists():
        connect = sqlite3.connect(str(database), **kwargs)

        with create_db_script.open('r') as f:
            sql = f.read()

        connect.executescript(sql)
        connect.commit()
        connect.close()


def dict_row_factory(cursor: Cursor, row: tuple) -> dict:
    """
    Фабрика результатов запроса.
    :param cursor: курсор результата запроса.
    :param row: кортеж строк результатов запроса.
    :return: словарь из результатов запроса.
    """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_connection(database: Path = settings.DATABASE,
                   row_factory: Optional[callable] = None,
                   **kwargs
                   ) -> Connection:
    """
    Возвращает коннект к БД.
    :param database: файл базы данных.
    :param row_factory: фабрика резульатов запроса.
    """
    connect = sqlite3.connect(str(database), **kwargs)

    if row_factory:
        connect.row_factory = row_factory

    return connect
