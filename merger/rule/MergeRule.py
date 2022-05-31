from abc import ABCMeta, abstractmethod
from typing import List

from common.const import MATH_OPERATOR_DICT
from common.stack import AstStack
from element.SQLCall import SQLCall
from element.SQLClause import SQLClause
from element.SQLElement import SQLElement
from element.SQLIdentifier import SQLIdentifier
from element.SQLOperator import SQLOperator
from element.SQLQuery import SQLQuery
from element.SQLLiteral import SQLLiteral
from lexical.KeyWord import SQLCommonKeyWord


class MergeRule(metaclass=ABCMeta):

    def validate(self, sql_elements):
        """校验
        :param sql_elements:
        :return:
        """
        pass

    @abstractmethod
    def trigger(self, element_stack: AstStack):
        """是否触发合并规则
        :param element_stack: sql元素栈
        :return: bool
        """
        pass

    @abstractmethod
    def action(self, element_stack: AstStack, rule_stack):
        """规则触发后的合并动作
        :param element_stack: sql元素栈
        :param rule_stack: 合并规则栈
        :return:
        """
        pass


class SQLQueryRule(MergeRule):

    def trigger(self, element_stack: AstStack):
        return True

    def action(self, element_stack: AstStack, rule_stack):

        sql_query = SQLQuery(None, None)

        # 子查询
        if element_stack.peek()[0].name == SQLCommonKeyWord.RIGHT_PARENTHESIS:
            first_idx = element_stack.index(SQLElement(name=SQLCommonKeyWord.LEFT_PARENTHESIS))
            pops = element_stack.popN(first_idx + 1)
            self.validate(pops[1:-1])

            start_pos = 1
            for i in range(1, len(pops)):
                if isinstance(pops[i].name, SQLCommonKeyWord) \
                        and pops[i].name.value[1].get('is_clause') and start_pos != i:
                    self._specify_clause(sql_query, start_pos, i, pops)
                    start_pos = i

            self._specify_clause(sql_query, start_pos, len(pops), pops)
            element_stack.pushElement(sql_query, rule_stack)

        # 最外层查询
        else:
            start_pos = 0
            pops = element_stack.popN(element_stack.getSize())
            self.validate(pops)

            for i in range(len(pops)):
                # todo: DeprecationWarning: using non-Enums in containment checks will raise TypeError in Python 3.8
                # 用python3.8的话需要修改
                if isinstance(pops[i].name, SQLCommonKeyWord) \
                        and pops[i].name.value[1].get('is_clause') and start_pos != i:
                    self._specify_clause(sql_query, start_pos, i, pops)
                    start_pos = i
            self._specify_clause(sql_query, start_pos, len(pops), pops)
            element_stack.pushElement(sql_query, rule_stack)

    def _specify_clause(self, sql_query, start_pos, i, pops):
        if pops[start_pos].name == SQLCommonKeyWord.SELECT:
            sql_query.selectList = list(filter(lambda x: x.name != SQLCommonKeyWord.COMMA, pops[start_pos + 1:i]))
        elif pops[start_pos].name == SQLCommonKeyWord.FROM:
            sql_query.from_ = pops[start_pos + 1:i][0]
        elif pops[start_pos].name == SQLCommonKeyWord.WHERE:
            sql_query.where = pops[start_pos + 1:i][0]
        elif pops[start_pos].name == SQLCommonKeyWord.GROUP:
            sql_query.group_by = list(filter(lambda x: x.name != SQLCommonKeyWord.COMMA, pops[start_pos + 2:i]))
        elif pops[start_pos].name == SQLCommonKeyWord.ORDER:
            order_by_list = []
            tmp_pops = pops[start_pos + 2:i]
            tmp_start = 0
            for i in range(len(tmp_pops)):
                if tmp_pops[i].name == SQLCommonKeyWord.COMMA:
                    if i - tmp_start == 1:
                        order_by_list.append(SQLCall(name=tmp_pops[tmp_start].name, alias=None,
                                                     operandList=[tmp_pops[tmp_start],
                                                                  SQLElement(SQLCommonKeyWord.ASC)]))
                    else:
                        order_by_list.append(SQLCall(name=tmp_pops[tmp_start].name, alias=None,
                                                     operandList=tmp_pops[tmp_start:i]))
                    tmp_start = i + 1
                if i == len(tmp_pops) - 1:
                    if i == tmp_start:
                        order_by_list.append(SQLCall(name=tmp_pops[tmp_start].name, alias=None,
                                                     operandList=[tmp_pops[tmp_start],
                                                                  SQLElement(SQLCommonKeyWord.ASC)]))
                    else:
                        order_by_list.append(SQLCall(name=tmp_pops[tmp_start].name, alias=None,
                                                     operandList=tmp_pops[tmp_start:i + 1]))
            sql_query.order_by = order_by_list
        elif pops[start_pos].name == SQLCommonKeyWord.LIMIT:
            sql_query.limit = SQLCall(name=None, alias=None, operator=None, operandList=list(
                filter(lambda x: x.name != SQLCommonKeyWord.COMMA, pops[start_pos + 1:i])))


class SpaceRule(MergeRule):

    # 当element栈栈顶不是空字符串时触发
    def trigger(self, element_stack):
        if element_stack.peek()[0].name in (SQLCommonKeyWord.SPACE,
                                            SQLCommonKeyWord.AS):
            return False
        return True

    def action(self, element_stack, rule_stack):
        pops = element_stack.popN(3)

        # 别名情况下的空格
        if (isinstance(pops[0], SQLIdentifier)
            or isinstance(pops[0], SQLCall)
            or isinstance(pops[0], SQLLiteral)) \
                and isinstance(pops[2], SQLIdentifier):

            pops[0].alias = pops[2].name
            element_stack.pushElement(pops[0], rule_stack)

        # 其他情况
        else:
            element_stack.pushElement(pops[0], rule_stack)
            element_stack.pushElement(pops[2], rule_stack)


class BinaryOperatorRule(MergeRule):

    # 当sql元素栈里操作符左右均为非sql call类型时触发
    def trigger(self, element_stack: AstStack):
        first_idx = element_stack.indexType(SQLOperator)
        elements = element_stack.peek(first_idx + 2)
        if len(elements) == 3 and not isinstance(elements[0], SQLCall) and not isinstance(elements[2], SQLCall):
            return True
        return False

    def action(self, element_stack: AstStack, rule_stack):
        pops = element_stack.popN(3)
        element = SQLCall(pops[1].name, alias=None, operator=pops[1], operandList=[pops[0], pops[2]])
        element.position = pops[1].position
        element_stack.pushElement(element, rule_stack)


class BoolBinaryOperatorRule(MergeRule):

    # 当sql元素栈里操作符左右均为sql call类型时触发
    def trigger(self, element_stack: AstStack):
        first_idx = element_stack.indexType(SQLOperator)
        elements = element_stack.peek(first_idx + 2)
        if len(elements) == 3 and isinstance(elements[0], SQLCall) and isinstance(elements[2], SQLCall):
            return True
        return False

    def action(self, element_stack: AstStack, rule_stack):
        pops = element_stack.popN(3)
        element = SQLCall(pops[1].name, alias=None, operator=pops[1], operandList=[pops[0], pops[2]])
        element.position = pops[1].position
        element_stack.pushElement(element, rule_stack)


class MathExpressRule(MergeRule):

    def __init__(self):
        self.elements = []

    def contains_operator(self, pops: List[SQLElement]):
        tmp_list = [pop.name for pop in pops]
        if SQLCommonKeyWord.ADD in tmp_list:
            return True
        if SQLCommonKeyWord.SUB in tmp_list:
            return True
        if SQLCommonKeyWord.ALL in tmp_list:
            return True
        if SQLCommonKeyWord.DIV in tmp_list:
            return True
        return False

    # 处理数据表达式
    def merge_expr(self, pops: List[SQLElement]):
        self.elements.extend(pops)
        # 基准优先级值, 遇到`(`需要加, 遇到`)`需要减
        base_priority = 0
        operator_priority_list = []
        parenthesis_idx_list = []
        for i in range(len(self.elements)):
            if self.elements[i].name == SQLCommonKeyWord.LEFT_PARENTHESIS:
                base_priority += MATH_OPERATOR_DICT[SQLCommonKeyWord.LEFT_PARENTHESIS]['priority']
                parenthesis_idx_list.append(i)
                continue
            if self.elements[i].name == SQLCommonKeyWord.RIGHT_PARENTHESIS:
                base_priority -= MATH_OPERATOR_DICT[SQLCommonKeyWord.RIGHT_PARENTHESIS]['priority']
                parenthesis_idx_list.append(i)
                continue
            if self.elements[i].name in MATH_OPERATOR_DICT.keys():
                # [操作符, 索引,操作符优先级值], 操作符优先级值=base_priority+该操作符的优先级值
                operator_priority_list.append(
                    [self.elements[i], i, MATH_OPERATOR_DICT[self.elements[i].name]['priority'] + base_priority])

        # drop掉括号, 更新操作符索引值, 并按优先级进行排序
        self.elements = list(filter(lambda x: x.name not in (SQLCommonKeyWord.LEFT_PARENTHESIS,
                                                             SQLCommonKeyWord.RIGHT_PARENTHESIS), self.elements))
        for each in operator_priority_list:
            each[1] -= len(list(filter(lambda x: each[1] > x, parenthesis_idx_list)))
        operator_priority_list.sort(key=lambda x: x[2], reverse=True)

        # 由于列表drop掉元素会导致index变化, 每次处理后需要更新`tokens`里元素的索引值
        for each in operator_priority_list:
            if not MATH_OPERATOR_DICT[each[0].name].get("is_function", 0):
                left_operand = self.elements.pop(each[1] - 1)
                math_operator = self.elements.pop(each[1] - 1)
                right_operand = self.elements.pop(each[1] - 1)
                element = SQLCall(operator=math_operator, operandList=[left_operand, right_operand])
                element.position = math_operator.position
                self.elements.insert(each[1] - 1, element)

                for tmp_each in operator_priority_list:
                    # 位于当前操作符后的操作符需要更新索引
                    if tmp_each[1] > each[1]:
                        tmp_each[1] -= 2
            else:
                func_operator = self.elements.pop(each[1])
                arg = self.elements.pop(each[1])
                element = SQLCall(operator=func_operator, operandList=[arg])
                element.position = func_operator.position
                self.elements.insert(each[1], element)
                for tmp_each in operator_priority_list:
                    if tmp_each[1] > each[1]:
                        tmp_each[1] -= 1

        return list(filter(lambda x: x, self.elements))

    def trigger(self, element_stack: AstStack):
        return True

    def action(self, element_stack: AstStack, rule_stack):
        first_idx = min(element_stack.index(SQLElement(SQLCommonKeyWord.COMMA)),
                        element_stack.index(SQLClause(SQLCommonKeyWord.SELECT)),
                        element_stack.index(SQLElement(SQLCommonKeyWord.LEFT_PARENTHESIS)))
        pops = element_stack.popN(first_idx)
        if self.contains_operator(pops):
            # todo: 删
            # if pops[-1].name == SQLCommonKeyWord.RIGHT_PARENTHESIS:
            #     element_stack.pushN(self.merge_expr(pops))
            # else:
            element_stack.pushN(self.merge_expr(pops[:-1]))
            element_stack.pushElement(pops[-1], rule_stack)
        else:
            element_stack.pushN(pops)


# sql关键字与对应的规则
RULE_DICT = {
    SQLCommonKeyWord.SPACE: SpaceRule,
    SQLCommonKeyWord.AS: SpaceRule,
    SQLCommonKeyWord.EQUAL: BinaryOperatorRule,
    SQLCommonKeyWord.GREATER_THAN: BinaryOperatorRule,
    SQLCommonKeyWord.LESS_THAN: BinaryOperatorRule,
    SQLCommonKeyWord.AND: BoolBinaryOperatorRule,
    SQLCommonKeyWord.OR: BoolBinaryOperatorRule
}
