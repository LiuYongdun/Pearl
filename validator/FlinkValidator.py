from common.const import SQL_CLAUSE_ORDER_DICT
from common.exception import SQLException
from element.SQLCall import SQLCall
from element.SQLClause import SQLClause
from element.SQLIdentifier import SQLIdentifier
from element.SQLQuery import SQLQuery
from lexical.KeyWord import SQLCommonKeyWord
from lexical.SQLDialect import SQLDialect
from validator.Validator import Validator


class FlinkSQLQueryValidator(Validator):

    def validate(self):
        self._validate_order()
        self._validate_select_cols()

    # 校验sql子句关键字顺序
    def _validate_order(self):
        # 只支持select开头的查询语句
        if self.sql_elements[0].name != SQLCommonKeyWord.SELECT:
            raise SQLException(self.sql_elements[0].position, "flink sql only supports select query")

        current_clause = 0
        for i in range(1, len(self.sql_elements)):
            if self.sql_elements[i].name in SQL_CLAUSE_ORDER_DICT[SQLDialect.FLINK_SQL].keys():
                # sql子句间需要有其他元素隔开
                if i - current_clause == 1:
                    raise SQLException(self.sql_elements[i].position,
                                       f"{self.sql_elements[i].name} can not directly follow {self.sql_elements[current_clause].name}")
                # 子句顺序需要正确
                if self.sql_elements[i].name not in SQL_CLAUSE_ORDER_DICT[SQLDialect.FLINK_SQL].get(
                        self.sql_elements[current_clause].name, []):
                    raise SQLException(self.sql_elements[i].position,
                                       f"{self.sql_elements[i].name} can not follow after {self.sql_elements[current_clause].name}")

                current_clause = i

    # 校验select字段
    def _validate_select_cols(self):
        # 校验逗号位置是否正确,是否连续
        col_end_idx = len(self.sql_elements)
        try:
            col_end_idx = self.sql_elements.index(SQLClause(SQLCommonKeyWord.FROM))
        except ValueError:
            pass

        for i in range(len(self.sql_elements[1:col_end_idx])):
            # 逗号只能出现在奇数位
            if self.sql_elements[1:col_end_idx][i].name == SQLCommonKeyWord.COMMA and i % 2 == 0:
                raise SQLException(self.sql_elements[1:col_end_idx][i].position,
                                   "comma should follow after column name")

        # 有子查询时,校验字段是否是子查询字段的子集
        if col_end_idx < len(self.sql_elements) and isinstance(self.sql_elements[col_end_idx + 1], SQLQuery):

            # 获取字段合集
            cols = []
            for each in self.sql_elements[1:col_end_idx]:
                if isinstance(each, SQLIdentifier):
                    cols.append(each.name)
                if isinstance(each, SQLCall):
                    cols.extend(self._get_col_identifiers_4_SQLCall(each))

            # 获取子查询字段合集
            sub_cols = []
            for each in self.sql_elements[col_end_idx + 1].selectList:
                if each.alias:
                    sub_cols.append(each.alias)
                else:
                    sub_cols.append(each.name)

            for col in cols:
                if col not in sub_cols:
                    raise SQLException(None, f"unknown column in select clause : {col}")

    # 递归获取SQLCall对象里的字段名称
    def _get_col_identifiers_4_SQLCall(self, sql_call):
        tmp_list = []
        for each in sql_call.operandList:
            if isinstance(each, SQLCall):
                tmp_list.extend(self._get_col_identifiers_4_SQLCall(each))
            elif isinstance(each, SQLIdentifier):
                tmp_list.append(each.name)
        return tmp_list
