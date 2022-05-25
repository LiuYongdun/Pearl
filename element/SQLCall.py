#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @Contact : Artle.Liu
# @Description : sql调用类型,包括函数,表达式


from element.SQLElement import SQLElement
from element.SQLOperator import SQLOperator
from typing import List


class SQLCall(SQLElement):

    def __init__(self, name, alias,
                 operator: SQLOperator = None,
                 operandList: List[SQLElement] = None):
        """
        :param operator: sql操作符,包括函数名,逻辑运算符,比较运算符等
        :param operandList: 操作数列表
        """
        super().__init__(name, alias)
        self.operator = operator
        self.operandList = operandList
