#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @Contact : Artle.Liu
# @Description : 数学表达式工具类

from element.SQLCall import SQLCall
from lexical.KeyWord import SQLCommonKeyWord


# 从ast重新生成数学表达式
def reconstruct(expr_ast):
    if len(expr_ast.operandList) == 1:
        if isinstance(expr_ast.operandList[0], SQLCall):
            child_str = reconstruct(expr_ast.operandList[0])
        elif all(map(lambda x: x.isdigit(), expr_ast.operandList[0].split('.'))) \
                and len(expr_ast.operandList[0].split('.')) <= 2:
            child_str = f"{expr_ast.operandList[0]}"
        else:
            child_str = f"`{expr_ast.operandList[0]}`"
        return f"{expr_ast.operator.value[0]}({child_str})"
    else:
        if isinstance(expr_ast.operandList[0], SQLCall):
            left_str = reconstruct(expr_ast.operandList[0])
        elif all(map(lambda x: x.isdigit(), expr_ast.operandList[0].split('.'))) \
                and len(expr_ast.operandList[0].split('.')) <= 2:
            left_str = f"{expr_ast.operandList[0]}"
        else:
            left_str = f"`{expr_ast.operandList[0]}`"

        if isinstance(expr_ast.operandList[1], SQLCall):
            right_str = reconstruct(expr_ast.operandList[1])
        elif all(map(lambda x: x.isdigit(), expr_ast.operandList[1].split('.'))) \
                and len(expr_ast.operandList[1].split('.')) <= 2:
            right_str = f"{expr_ast.operandList[1]}"
        else:
            right_str = f"`{expr_ast.operandList[1]}`"

        if expr_ast.operator == SQLCommonKeyWord.POW:
            return f"POWER{left_str, right_str}".replace("'", "")
        else:
            return f"({left_str} {expr_ast.operator.value[0]} {right_str})"
