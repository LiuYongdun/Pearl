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
from merger.rule.MergeRule import MathExpressRule
from common.stack import Stack


class FlinkMerger(Merger):

    def __init__(self):
        # sql元素栈和合并规则栈
        super().__init__()
        self.element_stack = AstStack()
        self.rule_stack = AstStack()

    def merge_sql(self, tokens):
        for token in tokens:
            if token['token_type']:
                # 操作符类型
                if token['token_type'] == SQLOperator:

                    # 合并规则入栈
                    if RULE_DICT.get(token['token_value']):
                        self.rule_stack.push(RULE_DICT.get(token['token_value']))
                        if token['token_value'] == SQLCommonKeyWord.AS:
                            self.rule_stack.push(MathExpressRule)
                    else:
                        raise AstException(f"no rule defined for operator type : {token['token_value']}")

                    # sql元素入栈
                    element = token['token_type'](name=token['token_value'],
                                                  operator_type=flink_operator_type_dict.get(token['token_value']))
                    element.position = Position(token['row_num'], token['col_num'])
                    self.element_stack.pushElement(element, self.rule_stack)

                # 空白字符串
                elif token['token_value'] == SQLCommonKeyWord.SPACE:
                    element = token['token_type'](name=token['token_value'], alias=None)
                    element.position = Position(token['row_num'], token['col_num'])
                    self.rule_stack.push(RULE_DICT.get(token['token_value']))
                    self.element_stack.pushElement(element, self.rule_stack)

                # 其他
                else:
                    if token['token_value'] in (SQLCommonKeyWord.FROM, SQLCommonKeyWord.COMMA):
                        self.rule_stack.push(MathExpressRule)
                    element = token['token_type'](name=token['token_value'], alias=None)
                    element.position = Position(token['row_num'], token['col_num'])
                    self.element_stack.pushElement(element, self.rule_stack)

        self.element_stack.pushElement(None, self.rule_stack)

        rule = FlinkSQLQueryRule()
        if rule.trigger(self.element_stack):
            rule.action(self.element_stack, self.rule_stack)

        return self.element_stack.pop()
