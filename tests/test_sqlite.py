from unittest import TestCase
from src.sqlite import split_sql_statement


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
