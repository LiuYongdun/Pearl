#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @Contact : Artle.Liu
# @Description : 常量文件

from lexical.KeyWord import SQLCommonKeyWord
from lexical.SQLDialect import SQLDialect

SQL_CLAUSE_ORDER_DICT = {
    SQLDialect.FLINK_SQL: {
        SQLCommonKeyWord.SELECT: [SQLCommonKeyWord.FROM],
        SQLCommonKeyWord.FROM: [SQLCommonKeyWord.WHERE, SQLCommonKeyWord.GROUP, SQLCommonKeyWord.ORDER,
                                SQLCommonKeyWord.LIMIT],
        SQLCommonKeyWord.WHERE: [SQLCommonKeyWord.GROUP, SQLCommonKeyWord.ORDER, SQLCommonKeyWord.LIMIT],
        SQLCommonKeyWord.GROUP: [SQLCommonKeyWord.HAVING, SQLCommonKeyWord.ORDER, SQLCommonKeyWord.LIMIT],
        SQLCommonKeyWord.HAVING: [SQLCommonKeyWord.ORDER, SQLCommonKeyWord.LIMIT],
        SQLCommonKeyWord.ORDER: [SQLCommonKeyWord.LIMIT],
        SQLCommonKeyWord.LIMIT: []
    }
}

# 数学表达式操作符优先级
MATH_OPERATOR_DICT = {
    SQLCommonKeyWord.ADD: {"priority": 1},
    SQLCommonKeyWord.SUB: {"priority": 1},
    # `*`号同时作为乘法符号和全部字段字符
    SQLCommonKeyWord.ALL: {"priority": 2},
    SQLCommonKeyWord.DIV: {"priority": 2},
    SQLCommonKeyWord.POW: {"priority": 3},
    SQLCommonKeyWord.SIN: {"priority": 4, "is_function": 1},
    SQLCommonKeyWord.TAN: {"priority": 4, "is_function": 1},
    SQLCommonKeyWord.COS: {"priority": 4, "is_function": 1},
    SQLCommonKeyWord.ARCCOS: {"priority": 4, "is_function": 1},
    SQLCommonKeyWord.ARCSIN: {"priority": 4, "is_function": 1},
    SQLCommonKeyWord.ARCTAN: {"priority": 4, "is_function": 1},
    SQLCommonKeyWord.ABS: {"priority": 4, "is_function": 1},
    SQLCommonKeyWord.LN: {"priority": 4, "is_function": 1},
    SQLCommonKeyWord.LG: {"priority": 4, "is_function": 1},
    SQLCommonKeyWord.LEFT_PARENTHESIS: {"priority": 5},
    SQLCommonKeyWord.RIGHT_PARENTHESIS: {"priority": 5}
}


