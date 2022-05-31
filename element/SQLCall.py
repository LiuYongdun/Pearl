#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @Contact : Artle.Liu
# @Description : sql调用类型,包括函数,表达式


from element.SQLElement import SQLElement
from element.SQLOperator import SQLOperator
from typing import List
from lexical.KeyWord import SQLCommonKeyWord


class SQLCall(SQLElement):

    def __init__(self, name=None, alias=None,
                 operator: SQLOperator = None,
                 operandList: List[SQLElement] = None):
        """
        :param operator: sql操作符,包括函数名,逻辑运算符,比较运算符等
        :param operandList: 操作数列表
        """
        super().__init__(name, alias)
        self.operator = operator
        self.operandList = operandList

    def __str__(self):
        if self.operator.name in (SQLCommonKeyWord.ADD,
                                  SQLCommonKeyWord.SUB,
                                  SQLCommonKeyWord.ALL,
                                  SQLCommonKeyWord.DIV):
            self.name = f"({self.operandList[0]}{self.operator.name.value[0]}{self.operandList[1]})"
        else:
            self.name = f"{self.operator.name.value[0]}({','.join(map(str, self.operandList))})"

        return super().__str__()
