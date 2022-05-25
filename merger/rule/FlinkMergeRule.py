#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @Contact : Artle.Liu
# @Description : flink sql合并规则

from abc import ABC

from common.exception import AstException
from common.stack import AstStack
from element.SQLCall import SQLCall
from element.SQLElement import SQLElement
from element.SQLOperator import SQLOperator, SQLOperatorType
from lexical.KeyWord import SQLCommonKeyWord, FlinkKeyWord
from merger.rule.MergeRule import MergeRule, SQLQueryRule, RULE_DICT
from validator.FlinkValidator import FlinkSQLQueryValidator


class FlinkSQLQueryRule(SQLQueryRule):

    def validate(self, sql_elements):
        FlinkSQLQueryValidator(sql_elements).validate()


class LeftParenthesisRule(MergeRule):

    # 当sql元素栈栈顶为右括号时触发
    def trigger(self, element_stack: AstStack):
        if element_stack.peek()[0].name == SQLCommonKeyWord.RIGHT_PARENTHESIS:
            return True
        return False

    def action(self, element_stack: AstStack, merge_rule_stack):
        first_idx = element_stack.index(SQLOperator(name=SQLCommonKeyWord.LEFT_PARENTHESIS,
                                                    operator_type=SQLOperatorType.LEFT_PARENTHESIS_OPERATOR))
        pops = element_stack.popN(first_idx + 2)

        if isinstance(pops[0], SQLElement):
            # 子查询的右括号
            if pops[0].name == SQLCommonKeyWord.FROM:
                element_stack.pushN(pops)
                rule = FlinkSQLQueryRule()
                if rule.trigger(element_stack):
                    rule.action(element_stack, merge_rule_stack)

            # 函数的右括号
            else:
                tmp_list = []
                for pop in pops:
                    if isinstance(pop.name, SQLCommonKeyWord) or isinstance(pop.name, FlinkKeyWord):
                        tmp_list.append(pop.name.value[0])
                    else:
                        tmp_list.append(pop.name)
                element = SQLCall(''.join(tmp_list), None,
                                  SQLOperator(pops[0].name, None, SQLOperatorType.FUNC_OPERATOR),
                                  list(filter(lambda x: x.name != SQLCommonKeyWord.COMMA, pops[2:-1])))
                element_stack.pushToken(element, merge_rule_stack)
        else:
            raise AstException("Unknown left parenthesis type, only support function and subquery parenthesis")


class IntervalFunctionRule(MergeRule):
    """
    flink interval 关键字当做函数处理,如: interval `10` second,将interval认为是函数名, 10和second当做参数
    """

    def trigger(self, element_stack: AstStack):
        if element_stack.peek(3)[0].name == FlinkKeyWord.INTERVAL:
            return True
        return False

    def action(self, element_stack: AstStack, merge_rule_stack):
        pops = element_stack.popN(3)
        tmp_list = []
        for pop in pops:
            if isinstance(pop.name, SQLCommonKeyWord) or isinstance(pop.name, FlinkKeyWord):
                tmp_list.append(pop.name.value[0])
            else:
                tmp_list.append(pop.name)
        element = SQLCall(' '.join(tmp_list), alias=None, operator=pops[0], operandList=pops[1:3])
        element_stack.pushToken(element, merge_rule_stack)


RULE_DICT = RULE_DICT.copy()
RULE_DICT.update({
    SQLCommonKeyWord.LEFT_PARENTHESIS: LeftParenthesisRule,
    FlinkKeyWord.INTERVAL: IntervalFunctionRule
})
