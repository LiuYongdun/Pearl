#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @Contact : Artle.Liu
# @Description : flink sql合并器类


from common.exception import AstException
from common.stack import AstStack
from element.SQLElement import Position
from element.SQLOperator import SQLOperator
from element.SQLOperator import flink_operator_type_dict
from lexical.KeyWord import SQLCommonKeyWord
from merger.Merger import Merger
from merger.rule.FlinkMergeRule import FlinkSQLQueryRule, RULE_DICT
from common.stack import Stack


class FlinkMerger(Merger):

    def __init__(self):
        # sql元素栈和合并规则栈
        super().__init__()
        self.sql_element_stack = AstStack()
        self.merge_rule_stack = Stack()

    def merge_sql(self, tokens):
        for token in tokens:
            if token['token_type']:
                # 操作符类型
                if token['token_type'] == SQLOperator:

                    # 合并规则入栈
                    if RULE_DICT.get(token['token_value']):
                        self.merge_rule_stack.push(RULE_DICT.get(token['token_value']))
                    else:
                        raise AstException(f"no rule defined for operator type : {token['token_value']}")

                    # sql元素入栈
                    element = token['token_type'](name=token['token_value'],
                                                  operator_type=flink_operator_type_dict.get(token['token_value']))
                    element.position = Position(token['row_num'], token['col_num'])
                    self.sql_element_stack.pushToken(element, self.merge_rule_stack)

                # 空白字符串
                elif token['token_value'] == SQLCommonKeyWord.SPACE:
                    element = token['token_type'](name=token['token_value'], alias=None)
                    element.position = Position(token['row_num'], token['col_num'])
                    self.merge_rule_stack.push(RULE_DICT.get(token['token_value']))
                    self.sql_element_stack.pushToken(element, self.merge_rule_stack)

                # 其他
                else:
                    element = token['token_type'](name=token['token_value'], alias=None)
                    element.position = Position(token['row_num'], token['col_num'])
                    self.sql_element_stack.pushToken(element, self.merge_rule_stack)

        self.sql_element_stack.pushToken(None, self.merge_rule_stack)

        rule = FlinkSQLQueryRule()
        if rule.trigger(self.sql_element_stack):
            rule.action(self.sql_element_stack, self.merge_rule_stack)

        return self.sql_element_stack.pop()
