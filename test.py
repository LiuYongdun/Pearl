import unittest

from lexical.SQLDialect import SQLDialect
from parser.SQLParser import SQLParserFactory


class AstTest(unittest.TestCase):

    def test_select(self):
        self.sql_parser = SQLParserFactory().produce(SQLDialect.FLINK_SQL)
        sql = """
        select c1 AS c2 from t_t1
            """
        sql_query = self.sql_parser.parse(sql)
        print(f"ast 测试:{sql_query}")


if __name__ == '__main__':
    unittest.main()
