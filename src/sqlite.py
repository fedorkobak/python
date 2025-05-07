import sqlite3
from typing import Any
from typeguard import typechecked


@typechecked
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


@typechecked
def execute_several_statements(
    cursor: sqlite3.Cursor | sqlite3.Connection,
    queries: str | list[str]
) -> list[tuple[Any, Any]]:
    """
    Execute multiple sql commands in the given `sqlite3.Cursor`.

    Parameters
    ----------
    cursor: sqlite3.Cursor
        Cursor where data should be executed.
    queries: str | list[str]
        Queries to run:
        - Can be a string with sql code where each quiery is separated by ";".
        - Can be a list of individual commands that supposed to be executed.

    Returns
    -------
    out: list[tuple[Any, Any]]
        List of the tuples where:
        - First element is `cursor.description`.
        - Second element is output of the `cursor.fetchall`.
    """
    if isinstance(queries, str):
        queries = split_sql_statement(code=queries)

    ans = []

    for query in queries:
        cursor.execute(query)
        ans.append((cursor.description, cursor.fetchall()))

    return ans
