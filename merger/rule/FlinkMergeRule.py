#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @Contact : Artle.Liu
# @Description : flink sql合并规则

from common.exception import AstException
from common.stack import AstStack
from element.SQLCall import SQLCall
from element.SQLElement import SQLElement
from element.SQLOperator import SQLOperator, SQLOperatorType
from lexical.KeyWord import SQLCommonKeyWord, FlinkKeyWord
from merger.rule.MergeRule import MergeRule, SQLQueryRule, MathExpressRule, RULE_DICT
from validator.FlinkValidator import FlinkSQLQueryValidator


class FlinkSQLQueryRule(SQLQueryRule):

    def validate(self, sql_elements):
        pass
        # FlinkSQLQueryValidator(sql_elements).validate()


class ParenthesisRule(MergeRule):

    # 当sql元素栈栈顶为右括号时触发
    def trigger(self, element_stack: AstStack):
        if element_stack.peek()[0].name == SQLCommonKeyWord.RIGHT_PARENTHESIS:
            return True
        return False

    def action(self, element_stack: AstStack, rule_stack: AstStack):

        rule_stack.push(MathExpressRule)
        element_stack.pushElement(None, rule_stack)
        first_idx = element_stack.index(SQLElement(name=SQLCommonKeyWord.LEFT_PARENTHESIS))
        if first_idx == element_stack.getSize():
            pass
        else:
            pops = element_stack.popN(first_idx + 2)
            if isinstance(pops[0], SQLElement):
                # 子查询的右括号
                if pops[0].name == SQLCommonKeyWord.FROM:
                    element_stack.pushN(pops)
                    rule_stack.push(FlinkSQLQueryRule)
                    element_stack.pushElement(None, rule_stack)

                # 函数的右括号
                elif pops[0].name.value[1].get("is_function"):
                    element = SQLCall(operator=SQLOperator(pops[0].name, None, SQLOperatorType.FUNC_OPERATOR),
                                      operandList=list(filter(lambda x: x.name != SQLCommonKeyWord.COMMA, pops[2:-1])))
                    element_stack.pushElement(element, rule_stack)

                else:
                    element_stack.push(pops[0])
                    for pop in pops[1:]:
                        if pop.name not in (SQLCommonKeyWord.LEFT_PARENTHESIS, SQLCommonKeyWord.RIGHT_PARENTHESIS):
                            element_stack.push(pop)
            else:
                raise AstException("unknown left parenthesis type, only support function and subquery parenthesis")


class IntervalFunctionRule(MergeRule):
    """
    flink interval 关键字当做函数处理,如: interval `10` second,将interval认为是函数名, 10和second当做参数
    """

    def trigger(self, element_stack: AstStack):
        if element_stack.peek(3)[0].name == FlinkKeyWord.INTERVAL:
            return True
        return False

    def action(self, element_stack: AstStack, rule_stack):
        pops = element_stack.popN(3)
        tmp_list = []
        for pop in pops:
            if isinstance(pop.name, SQLCommonKeyWord) or isinstance(pop.name, FlinkKeyWord):
                tmp_list.append(pop.name.value[0])
            else:
                tmp_list.append(pop.name)
        element = SQLCall(' '.join(tmp_list), alias=None, operator=pops[0], operandList=pops[1:3])
        element_stack.pushElement(element, rule_stack)


RULE_DICT = RULE_DICT.copy()
RULE_DICT.update({
    SQLCommonKeyWord.RIGHT_PARENTHESIS: ParenthesisRule,
    FlinkKeyWord.INTERVAL: IntervalFunctionRule
})
