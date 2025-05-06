import sqlite3
from typing import Any


def split_sql_statement(code: str) -> list[str]:
    """
    Splits multi-command SQL statement into a list of strings, where each
    element is an SQL statement.

    Parameters
    ----------
    code: str
        SQL code that needs to be separated into unit commands.

    Returns
    -------
    list[str]
    """
    res: list[str] = code.split(";")
    res = [command.strip() for command in res]

    # If there is no any text after the last ';', remove everything.
    if res[-1].strip() == "":
        del res[-1]

    return res


def execute_several_statements(
    cursor: sqlite3.Cursor,
    queries: str | list[str]
) -> list[tuple[Any, Any]]:
    # statements = split_sql_statement(queries)
    pass
