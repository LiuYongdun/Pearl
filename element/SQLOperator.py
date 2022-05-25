#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @Contact : Artle.Liu
# @Description : sql操作符

from enum import Enum, unique
from element.SQLElement import SQLElement
from lexical.KeyWord import FlinkKeyWord


@unique
class SQLOperatorType(Enum):
    LOGIC_OPERATOR = 0
    LEFT_PARENTHESIS_OPERATOR = 1
    RELATION_OPERATOR = 2
    FUNC_OPERATOR = 3
    SELECT_OPERATOR = 4
    FROM_OPERATOR = 5
    WHERE_OPERATOR = 6
    GROUP_OPERATOR = 7
    ORDER_OPERATOR = 8
    LIMIT_OPERATOR = 9
    RIGHT_PARENTHESIS_OPERATOR = 10


class SQLOperator(SQLElement):
    def __init__(self, name, alias=None, operator_type: SQLOperatorType = None):
        super().__init__(name, alias)
        self.operator_type = operator_type

    # todo: 看一下有没有用, 没有就删了
    def __str__(self):
        return str({"class": SQLOperator,
                    "fields": {"name": self.name, "alias": self.alias, "operator_type": self.operator_type}})


flink_operator_type_dict = {
    FlinkKeyWord.LEFT_PARENTHESIS: SQLOperatorType.LEFT_PARENTHESIS_OPERATOR,
    FlinkKeyWord.RIGHT_PARENTHESIS: SQLOperatorType.RIGHT_PARENTHESIS_OPERATOR,
    FlinkKeyWord.EQUAL: SQLOperatorType.RELATION_OPERATOR,
    FlinkKeyWord.AND: SQLOperatorType.LOGIC_OPERATOR,
    FlinkKeyWord.OR: SQLOperatorType.LOGIC_OPERATOR,
    FlinkKeyWord.MAX: SQLOperatorType.FUNC_OPERATOR,
    FlinkKeyWord.SELECT: SQLOperatorType.SELECT_OPERATOR,
    FlinkKeyWord.FROM: SQLOperatorType.FROM_OPERATOR,
    FlinkKeyWord.WHERE: SQLOperatorType.WHERE_OPERATOR,
    FlinkKeyWord.GREATER_THAN: SQLOperatorType.RELATION_OPERATOR,
    FlinkKeyWord.GROUP: SQLOperatorType.GROUP_OPERATOR
}
