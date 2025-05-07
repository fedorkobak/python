from unittest import TestCase
from unittest.mock import patch, MagicMock

import src.sqlite
from src.sqlite import split_sql_statement, execute_several_statements


class TestSplitStatement(TestCase):
    def test_sql_split(self):
        inp = """
        SELECT 10; SELECT 20;
        INSERT SOME HELLO;
        """
        out = split_sql_statement(inp)
        exp_out = [
            "SELECT 10",
            "SELECT 20",
            "INSERT SOME HELLO"
        ]
        self.assertEqual(out, exp_out)


class TestExecuteSeveralStatements(TestCase):

    @patch.object(src.sqlite, "split_sql_statement")
    def test_string_input(self, split_function: MagicMock):
        """
        Test case when function takes string as input.

        1. `split_sql_statements` must be called with an input string.
        2. `cursor.execute` must be called on each query.
        """
        input_query = """
        query1; query2; query3;
        """
        split_function.return_value = ["query1", "query2", "query3"]

        cursor = MagicMock()
        execute_several_statements(cursor=cursor, queries=input_query)

        split_function.assert_called_once_with(code=input_query)

        executed_queries = [call.args[0] for call in cursor.execute.mock_calls]
        self.assertEqual(executed_queries, split_function.return_value)
