#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @Contact : Artle.Liu
# @Description : sql解析器基类

import re
from abc import ABCMeta, abstractmethod
from common.exception import AstException
from lexical.KeyWord import SQLCommonKeyWord, FlinkKeyWord
from lexical.Lexer import Lexer
from lexical.SQLDialect import SQLDialect
from merger.FlinkMerger import FlinkMerger


class SQLParser(metaclass=ABCMeta):

    @abstractmethod
    def _format(self, sql: str) -> str:
        """格式化sql字符串
        :param sql:
        :return:
        """
        pass

    @abstractmethod
    def parse(self, sql: str):
        """解析sql成抽象语法树
        :param sql:
        :return:
        """
        pass


class FlinkSQLParser(SQLParser):

    def _format(self, sql):
        sql = re.sub('[;]', ' ', sql.lower()).strip()
        special_chars = [each.value[0] for each in SQLCommonKeyWord if each.value[1].get('is_special_char')]
        for kw in FlinkKeyWord:
            if kw.value[0] not in special_chars:
                sql = re.sub(f'\\b{kw.value[0].lower()}\\b', kw.value[0], sql)
        return sql

    def parse(self, sql):
        tokens = Lexer(SQLDialect.FLINK_SQL).tokenize(self._format(sql))
        list(map(print, tokens))
        sql_query = FlinkMerger().merge_sql(tokens)
        return sql_query


class SQLParserFactory:

    parser_dict = {
        SQLDialect.FLINK_SQL: FlinkSQLParser
    }

    def produce(self, sql_dialect: SQLDialect):
        parser = self.parser_dict.get(sql_dialect)
        if parser:
            return parser()
        else:
            raise AstException(f"no parser defined for sql dialect: {sql_dialect}")
