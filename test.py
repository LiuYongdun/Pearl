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
        print()

    def test_subquery(self):
        self.sql_parser = SQLParserFactory().produce(SQLDialect.FLINK_SQL)
        sql = """
        select c1 from (select c1 from t_t1)
            """
        sql_query = self.sql_parser.parse(sql)
        print()

    def test_expr1(self):
        self.sql_parser = SQLParserFactory().produce(SQLDialect.FLINK_SQL)

        sql = '''
            select a+b/4 from t1
        '''
        sql_query = self.sql_parser.parse(sql)
        print()

    def test_expr2(self):
        self.sql_parser = SQLParserFactory().produce(SQLDialect.FLINK_SQL)

        sql = '''
            select c1, max(a+b/4) from t1
        '''
        sql_query = self.sql_parser.parse(sql)
        print()

    def test_expr3(self):
        self.sql_parser = SQLParserFactory().produce(SQLDialect.FLINK_SQL)

        sql = '''
            select c1, (a +b / 4 ) AS c1 from t1
        '''
        sql_query = self.sql_parser.parse(sql)
        print()

    def test_expr4(self):
        self.sql_parser = SQLParserFactory().produce(SQLDialect.FLINK_SQL)

        sql = '''
            select a+b/4 AS c3, c1 AS c2 from t1
        '''
        sql_query = self.sql_parser.parse(sql)
        print()

    def test_expr5(self):
        self.sql_parser = SQLParserFactory().produce(SQLDialect.FLINK_SQL)

        sql = '''
            select 'a+b/4', '33ddsd' from t1
        '''
        sql_query = self.sql_parser.parse(sql)
        print()

    def test_expr6(self):
        self.sql_parser = SQLParserFactory().produce(SQLDialect.FLINK_SQL)

        sql = '''
            select 'a+b/4' AS a1 , max(( c1+ c2 )/4-LN(c1) ) AS c3 from t1
        '''
        sql_query = self.sql_parser.parse(sql)
        print()


if __name__ == '__main__':
    unittest.main()
