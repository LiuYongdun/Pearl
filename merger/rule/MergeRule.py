from abc import ABCMeta, abstractmethod, ABC

from common.stack import AstStack
from element.SQLCall import SQLCall
from element.SQLClause import SQLClause
from element.SQLElement import SQLElement
from element.SQLIdentifier import SQLIdentifier
from element.SQLOperator import SQLOperator, SQLOperatorType
from element.SQLQuery import SQLQuery
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
    def action(self, element_stack: AstStack, merge_rule_stack):
        """规则触发后的合并动作
        :param element_stack: sql元素栈
        :param merge_rule_stack: 合并规则栈
        :return:
        """
        pass


class SQLQueryRule(MergeRule):

    def trigger(self, element_stack: AstStack):
        return True

    def action(self, element_stack: AstStack, merge_rule_stack):

        sql_query = SQLQuery(None, None)

        # 子查询
        if element_stack.peek()[0].name == SQLCommonKeyWord.RIGHT_PARENTHESIS:
            first_idx = element_stack.index(SQLOperator(name=SQLCommonKeyWord.LEFT_PARENTHESIS,
                                                        operator_type=SQLOperatorType.LEFT_PARENTHESIS_OPERATOR))
            pops = element_stack.popN(first_idx + 1)
            self.validate(pops[1:-1])

            start_pos = 1
            for i in range(1, len(pops)):
                if isinstance(pops[i].name, SQLCommonKeyWord) \
                        and pops[i].name.value[1].get('is_clause') and start_pos != i:
                    self._specify_clause(sql_query, start_pos, i, pops)
                    start_pos = i

            self._specify_clause(sql_query, start_pos, len(pops), pops)
            element_stack.pushToken(sql_query, merge_rule_stack)

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
            element_stack.pushToken(sql_query, merge_rule_stack)

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

    # 当sql元素栈栈顶不是空字符串时触发
    def trigger(self, element_stack):
        if element_stack.peek()[0].name in (SQLCommonKeyWord.SPACE, SQLCommonKeyWord.AS):
            return False
        return True

    def action(self, element_stack, merge_rule_stack):
        pops = element_stack.popN(3)

        # 别名情况下的空格
        if not isinstance(pops[0], SQLClause) \
                and not isinstance(pops[0], SQLOperator) \
                and pops[0].name not in (SQLCommonKeyWord.BY, SQLCommonKeyWord.COMMA, SQLCommonKeyWord.SPACE) \
                and isinstance(pops[2], SQLIdentifier):

            pops[0].alias = pops[2].name
            element_stack.pushToken(pops[0], merge_rule_stack)

        # 其他情况
        else:
            element_stack.pushToken(pops[0], merge_rule_stack)
            element_stack.pushToken(pops[2], merge_rule_stack)


class BinaryOperatorRule(MergeRule):

    # 当sql元素栈里操作符左右均为非sql call类型时触发
    def trigger(self, element_stack: AstStack):
        first_idx = element_stack.indexType(SQLOperator)
        elements = element_stack.peek(first_idx + 2)
        if len(elements) == 3 and not isinstance(elements[0], SQLCall) and not isinstance(elements[2], SQLCall):
            return True
        return False

    def action(self, element_stack: AstStack, merge_rule_stack):
        pops = element_stack.popN(3)
        element = SQLCall(pops[1].name, alias=None, operator=pops[1], operandList=[pops[0], pops[2]])
        element_stack.pushToken(element, merge_rule_stack)


class BoolBinaryOperatorRule(MergeRule):

    # 当sql元素栈里操作符左右均为sql call类型时触发
    def trigger(self, element_stack: AstStack):
        first_idx = element_stack.indexType(SQLOperator)
        elements = element_stack.peek(first_idx + 2)
        if len(elements) == 3 and isinstance(elements[0], SQLCall) and isinstance(elements[2], SQLCall):
            return True
        return False

    def action(self, element_stack: AstStack, merge_rule_stack):
        pops = element_stack.popN(3)
        element = SQLCall(pops[1].name, alias=None, operator=pops[1], operandList=[pops[0], pops[2]])
        element_stack.pushToken(element, merge_rule_stack)


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
