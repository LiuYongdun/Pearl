#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @Contact : Artle.Liu
# @Description : sql语法树合并器基类

from abc import ABCMeta, abstractmethod
from typing import List, Dict
from common.const import MATH_OPERATOR_DICT
from element.SQLCall import SQLCall
from lexical.KeyWord import SQLCommonKeyWord


class Merger(metaclass=ABCMeta):

    def __init__(self):
        self.math_tokens = []

    # 处理整体的sql语句, 不包括数学表达式
    @abstractmethod
    def merge_sql(self, tokens: List[Dict]):
        pass

    # 处理数据表达式
    # def merge_expr(self, tokens: List):
    #     self.math_tokens.extend([token['token_value'] for token in tokens])
    #     # 基准优先级值, 遇到`(`需要加, 遇到`)`需要减
    #     base_priority = 0
    #     operator_priority_list = []
    #     parenthesis_idx_list = []
    #     for i in range(len(self.math_tokens)):
    #         if self.math_tokens[i] == SQLCommonKeyWord.LEFT_PARENTHESIS:
    #             base_priority += MATH_OPERATOR_DICT[SQLCommonKeyWord.LEFT_PARENTHESIS]['priority']
    #             parenthesis_idx_list.append(i)
    #             continue
    #         if self.math_tokens[i] == SQLCommonKeyWord.RIGHT_PARENTHESIS:
    #             base_priority -= MATH_OPERATOR_DICT[SQLCommonKeyWord.RIGHT_PARENTHESIS]['priority']
    #             parenthesis_idx_list.append(i)
    #             continue
    #         if self.math_tokens[i] in MATH_OPERATOR_DICT.keys():
    #             # [操作符, 索引,操作符优先级值], 操作符优先级值=base_priority+该操作符的优先级值
    #             operator_priority_list.append(
    #                 [self.math_tokens[i], i, MATH_OPERATOR_DICT[self.math_tokens[i]]['priority'] + base_priority])
    #
    #     # drop掉括号, 更新操作符索引值, 并按优先级进行排序
    #     self.math_tokens = list(filter(lambda x: x not in (SQLCommonKeyWord.LEFT_PARENTHESIS,
    #                                                        SQLCommonKeyWord.RIGHT_PARENTHESIS), self.math_tokens))
    #     for each in operator_priority_list:
    #         each[1] -= len(list(filter(lambda x: each[1] > x, parenthesis_idx_list)))
    #     operator_priority_list.sort(key=lambda x: x[2], reverse=True)
    #
    #     # 由于列表drop掉元素会导致index变化, 每次处理后需要更新`tokens`里元素的索引值
    #     for each in operator_priority_list:
    #
    #         if not MATH_OPERATOR_DICT[each[0]].get("is_function", 0):
    #             left_operand = self.math_tokens.pop(each[1] - 1)
    #             math_operator = self.math_tokens.pop(each[1] - 1)
    #             right_operand = self.math_tokens.pop(each[1] - 1)
    #             self.math_tokens.insert(each[1] - 1, SQLCall(name=None, alias=None, operator=math_operator,
    #                                                          operandList=[left_operand, right_operand]))
    #
    #             for tmp_each in operator_priority_list:
    #                 # 位于当前操作符后的操作符需要更新索引
    #                 if tmp_each[1] > each[1]:
    #                     tmp_each[1] -= 2
    #         else:
    #             function_name = self.math_tokens.pop(each[1])
    #             arg = self.math_tokens.pop(each[1])
    #             self.math_tokens.insert(each[1],
    #                                     SQLCall(name=None, alias=None, operator=function_name, operandList=[arg]))
    #             for tmp_each in operator_priority_list:
    #                 if tmp_each[1] > each[1]:
    #                     tmp_each[1] -= 1
    #
    #     return list(filter(lambda x: x, self.math_tokens))[0]
