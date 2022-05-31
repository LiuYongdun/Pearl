#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @Contact : Artle.Liu (Artle.Liu@fatritech.com)
# @Description : sql词法分析器

import re
from itertools import chain
from typing import List, Dict
from element.SQLClause import SQLClause
from element.SQLElement import SQLElement
from element.SQLIdentifier import SQLIdentifier
from element.SQLLiteral import SQLLiteral
from element.SQLOperator import SQLOperator
from lexical.KeyWord import SQLCommonKeyWord, FlinkKeyWord
from lexical.SQLDialect import SQLDialect


class Lexer:
    keyword_dict = {
        SQLDialect.FLINK_SQL: FlinkKeyWord
    }

    def __init__(self, sql_dialect: SQLDialect):
        self.sql_dialect = sql_dialect

    # 确定w_token的类型:{sql操作符关键字,sql其他关键字,sql字面量,字段名和别名等标识符}
    def _specify_w_token_type(self, token_value: str):
        for each in chain(SQLCommonKeyWord, self.keyword_dict[self.sql_dialect]):
            if token_value.upper() == each.value[0].upper():
                if not each.value[1].get('is_operator'):
                    return (SQLClause, each) if each.value[1].get('is_clause') else (SQLElement, each)
                else:
                    return SQLOperator, each
        if re.match('(^[0-9]*$|^\'.*\'$)', token_value):
            return SQLLiteral, token_value
        else:
            return SQLIdentifier, token_value

    # 确定非w_token的类型:sql关键字同时为操作符,其他sql关键字,其他类型
    def _specify_nw_token_type(self, token_value: str):
        for each in chain(SQLCommonKeyWord, self.keyword_dict[self.sql_dialect]):
            if token_value.upper() == each.value[0].upper():
                return (SQLElement, each) if not each.value[1].get('is_operator') else (SQLOperator, each)
            if re.match('^ +$', token_value.upper()):
                return SQLElement, SQLCommonKeyWord.SPACE

        return None, token_value

    def tokenize(self, sql: str) -> List[Dict]:
        """分词
        :param sql: sql语句
        :return: token列表
        """
        tokens = []
        start_pos = 0
        row_num = 1
        col_num = 1

        # 将token分为两类,一类是以'[0-9a-zA-Z_]'组成的word_token(sql关键字,字段名等),其他的token归为第二类(逗号,括号,空白字符串等)
        w_token_start = True
        str_token_start = False
        w_token_regex = '[0-9a-zA-Z_.\'`]'

        for i in range(len(sql)):

            if sql[i] == '\'':
                str_token_start = not str_token_start

            # 当前位置的字符属于word_token,则继续往下读,直到遇见非word_token的字符
            if w_token_start:
                if re.match(w_token_regex, sql[i]) or str_token_start:
                    continue
                else:
                    w_token_start = False
                    token_type, token_value = self._specify_w_token_type(sql[start_pos:i])
                    tokens.append({"token_type": token_type, "token_value": token_value,
                                   "row_num": row_num, "col_num": col_num})
            else:
                # 空格字符继续读
                if re.match(' ', sql[i]) and re.match(' ', sql[i - 1]):
                    continue
                elif not re.match(w_token_regex, sql[i]):
                    w_token_start = False
                    token_type, token_value = self._specify_nw_token_type(sql[start_pos:i])
                    tokens.append({"token_type": token_type, "token_value": token_value,
                                   "row_num": row_num, "col_num": col_num})
                else:
                    w_token_start = True
                    token_type, token_value = self._specify_nw_token_type(sql[start_pos:i])
                    tokens.append({"token_type": token_type, "token_value": token_value,
                                   "row_num": row_num, "col_num": col_num})

            # 行号和列号更新
            if sql[i] == '\n':
                row_num += 1
                col_num = 0
            else:
                col_num += i - start_pos
            start_pos = i

        # 最后一个token
        token_type, token_value = self._specify_w_token_type(sql[start_pos:len(sql)])
        tokens.append({"token_type": token_type, "token_value": token_value,
                       "row_num": row_num, "col_num": col_num})

        return tokens


if __name__ == '__main__':
    _sql = "92^2+(2*3)-4/2"
    for _ in Lexer(SQLDialect.FLINK_SQL).tokenize(_sql):
        print(_)
